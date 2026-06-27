"""Analysis prompt — the core prompt for deep document reading and entity extraction.

This prompt is sent for each document. It includes:
1. The seed context (permanent background)
2. The 17-type meta-model (classification reference)
3. Accumulated knowledge from previous documents
4. The current document content
"""

from context_blocks.config import get_settings
from context_blocks.infrastructure.llm.token_utils import truncate_if_needed
from context_blocks.meta_model import format_meta_model_for_prompt
from context_blocks.models.summary import KnowledgeSummary


SYSTEM_PROMPT = """You are a brilliant new team member reading enterprise documentation to deeply understand a domain. You are NOT a search indexer or keyword extractor. You READ documents the way an experienced architect would — understanding intent, relationships, business context, and the reasoning behind decisions.

Your job is to read a single document and extract structured domain entities from it. Every entity you extract MUST be classified into one of the 18 entity types defined in the meta-model below.

## How to Read

- Read the ENTIRE document before extracting anything. Understand it first.
- Think about what this document TEACHES about the domain — not just what words it contains.
- Look for systems, processes, business rules, terminology, decisions, events, infrastructure, and relationships.
- If something is implied but not stated explicitly, note it as a question — don't invent.
- If a concept doesn't clearly fit one entity type, use status "proposed" and suggest which type it might be.
- If you discover domain terms not in the seed context jargon list, flag them as new jargon.
- If the document contains dates, note how old the information is. Tag entities from old documents (3+ years) with 'legacy-era' or similar.
- If you encounter passwords, API keys, secrets, tokens, or credentials, flag them as a security concern in your questions. Do NOT include the actual secret in entity content.

## What Makes a Good Entity

- An entity is a CONCEPT worth remembering, not a mention of a word.
- A named system that processes orders → entity (type: system)
- A named database that stores domain data → entity (type: software-component)
- A named event flow between two systems → entity (type: business-event)
- A named event flow or data exchange between systems → entity (type: business-event). Extract EVERY distinct event — if a diagram shows 5 arrows between systems, that's potentially 5 business events.
- A generic technology mentioned without domain context ("we use REST") → NOT an entity
- Each entity should have enough detail that someone reading ONLY the entity file would understand what it is and why it matters.
- Every named component with its own identity and purpose deserves its own entity. If a document names 7 distinct components, create 7 entities. Short detail is fine — later documents will enrich them.
- Relationships should capture how entities connect in THIS domain. For each entity type, actively look for the EXPECTED relationships listed in the meta-model. Also add generic relationships (depends_on, related_to) when applicable. If ownership is unclear, flag it.

## Diagrams

- For process entities, include a Mermaid diagram in the details if you can express the flow visually. Use flowcharts for processes, sequence diagrams for integrations.
- For any entity where a diagram genuinely clarifies the content, add it using Mermaid syntax within the markdown.
- Only add diagrams when they genuinely clarify — don't force them.

## What NOT to Do

- Don't consolidate distinct named things into a single entity — if a document names 4 separate services, extract 4 entities
- Don't skip extracting something just because the seed context already mentions it — create the full entity anyway
- Use the EXACT name from the document. Don't add suffixes like '-service', '-system', or '-component' unless the document uses them. If the document says "Pricing", the entity name is "Pricing", not "Pricing Service"
- Don't create entities for things only mentioned in passing with no context
- Don't fabricate relationships you're not confident about
- Entity IDs should NOT include the entity type as a prefix. Files are organized into folders by type (e.g., `jargon-business/`, `systems/`, `decisions/`), so an entity ID like `billable-unit` is correct — NOT `jargon-bu` or `jargon-billable-unit`. The ID should be the concept name in kebab-case, nothing more.
"""


def build_system_prompt(seed_context: str) -> str:
    """Build the cacheable system prompt (stable across all document calls).

    This combines SYSTEM_PROMPT + seed context + meta-model into one block
    that Anthropic caches in GPU memory. Cached tokens get 90% input discount.

    Args:
        seed_context: The full seed context markdown content.

    Returns:
        Combined system prompt string (~6,200 tokens, all cacheable).
    """
    meta_model = format_meta_model_for_prompt()

    return f"""{SYSTEM_PROMPT}

---

## Seed Context (your day-1 onboarding walkthrough — permanent background)

{seed_context}

---

{meta_model}"""


def build_analysis_prompt(
    document_content: str,
    document_filename: str,
    seed_context: str,
    knowledge_summary: KnowledgeSummary | None,
    retrieved_entities: str = "",
    existing_entity_ids: list[dict[str, str]] | None = None,
) -> str:
    """Build the dynamic user prompt for a single document.

    This contains only the parts that change per call: knowledge summary,
    entity tree, and document content. The stable parts (seed context,
    meta-model, system instructions) are in the system prompt via
    build_system_prompt() and get cached.

    Args:
        document_content: The text content of the document to analyze.
        document_filename: The filename for reference.
        seed_context: The full seed context (used only for truncation calc).
        knowledge_summary: Fixed-size summary from previous documents (None for first doc).
        retrieved_entities: Formatted string of relevant previously-extracted entities.

    Returns:
        The user prompt string to send to the LLM.
    """
    # Build knowledge context section
    if knowledge_summary:
        knowledge_section = knowledge_summary.to_prompt_text()
    else:
        knowledge_section = (
            "This is your first document. The seed context above is your only background. "
            "Read this document carefully — it will form the foundation of your domain understanding."
        )

    # Build retrieved entities section
    retrieved_section = ""
    if retrieved_entities:
        retrieved_section = f"""
---

{retrieved_entities}
"""

    # Build existing entity ID list grouped by type
    entity_id_section = ""
    if existing_entity_ids:
        entity_id_section = _format_entity_id_tree(existing_entity_ids)

    # Truncate document if it would exceed context window
    settings = get_settings()
    accumulated_text = knowledge_section + retrieved_section + entity_id_section
    document_content = truncate_if_needed(
        document_content=document_content,
        seed_context=seed_context,
        accumulated_text=accumulated_text,
        model=settings.llm_model,
    )

    from datetime import date
    today = date.today().isoformat()

    return f"""**Today's date: {today}** — use this to assess how old document content is. If a document references dates from 3+ years ago, tag entities with 'legacy-era'.

## Your Current Domain Understanding

{knowledge_section}
{retrieved_section}
{entity_id_section}
---

## Document to Analyze

**Filename:** {document_filename}

{document_content}

---

## Your Task

You are building a reverse knowledge transfer documentation that would impress the domain experts on this team. "Impress" means:
- You connect things they didn't expect a new joiner to connect
- You identify things the team takes for granted but never documented
- You ask questions that show deep understanding, not surface confusion
- You use domain language correctly, not just parroted
- You capture WHY things are the way they are, not just WHAT they are

Read the document above thoroughly. Then extract:

1. **Entities** — every distinct named concept in this document. Each named system, service, component, process, event flow, or decision that has its own identity and purpose is its own entity. Never consolidate distinct named things into a single entity.

   Your job is to BUILD KNOWLEDGE — both creating new entities AND enriching existing ones. When you encounter something in a document that matches an existing entity (even under a different name), use the existing entity's ID and include whatever new information this document reveals. The system will merge your additions with the existing file. Never skip something because it already exists — every document adds new perspective.

   For each entity provide:
   - The entity type (from the meta-model)
   - A kebab-case ID
   - A human-readable name
   - A one-line description
   - A 2-3 sentence overview
   - Detailed explanation with specifics
   - Relationships to other entities (including ownership if known, flag if unclear)
   - Your confidence level (0.0-1.0) and reasoning for the classification
   - Tags for filtering: use labels like 'infrastructure', 'upstream', 'downstream', 'domain-logic', 'conflict', 'low-confidence', 'needs-review', 'seed-context-derived' (for entities created from seed context rather than the document)
   - If something important doesn't fit any entity type, use status "proposed" and suggest which type it might be

2. **Questions** — anything ambiguous, unclear, or that you'd want to ask a domain expert about

3. **New jargon** — domain terms you encountered that weren't in the seed context jargon list

4. **Decision log** — for each significant decision you made, explain your reasoning:
   - Why you classified something as a particular entity type
   - Why you skipped something (chose not to create an entity)
   - Why you reused an existing entity ID vs creating a new one
   - Any conflicts you noticed between this document and previous knowledge

   This log is for debugging and calibration — be honest about uncertainty.

**Important on hedged language:** When writing entity content, if you use words like 'maybe', 'likely', 'appears to', 'seems', 'could be', 'probably' — keep them in the content (honesty is good) BUT also add each hedged statement to that entity's `hedged_statements` field, rephrased as a question a domain expert could confirm or deny. This happens PER ENTITY as you write it, not as a post-scan."""


def _format_entity_id_tree(entities: list[dict[str, str]]) -> str:
    """Format existing entity IDs as a typed tree for the prompt.

    Output looks like:
    ### Existing Entities (12 total)
    **systems:** order-processor (Order Processor), payment-engine (Payment Engine)
    **software-components:** orders-postgres-db (Orders PostgreSQL Database)
    **apis:** orders-rest-api (Orders REST API)
    """
    # Group by type
    by_type: dict[str, list[dict[str, str]]] = {}
    for entity in entities:
        t = entity["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(entity)

    lines = [
        "",
        "---",
        "",
        f"### Existing Entities ({len(entities)} total)",
        "",
        "If you're extracting something that IS one of these, use the EXACT same ID and type. "
        "Check both the name AND the type — the same concept can exist as different entity types "
        "(e.g., 'order-processor' as a system vs 'order-processor-db' as a software-component).",
        "",
    ]

    for entity_type in sorted(by_type.keys()):
        items = by_type[entity_type]
        entries = ", ".join(f"{e['id']} ({e['name']})" for e in items)
        lines.append(f"**{entity_type}:** {entries}")

    lines.append("")

    return "\n".join(lines)
