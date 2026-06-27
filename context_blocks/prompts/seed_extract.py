"""Seed context extraction prompt — creates foundation entities from the seed context.

This runs ONCE before any document analysis. The seed context is human-written
and the most reliable source of domain knowledge. Entities created here form
the skeleton that documents flesh out.
"""


SEED_EXTRACT_SYSTEM_PROMPT = """You are reading a human-written onboarding document for a domain. This is the most reliable source of information — it was written intentionally by someone who knows the domain.

Your job is to extract FOUNDATION entities from this document. These become the skeleton of the domain knowledge base. Later, when analyzing actual documentation, these entities will be enriched with details.

Create entities for everything explicitly mentioned:
- Named systems and services → system entities
- Named teams → team entities
- Named people roles → persona entities
- Named external parties (suppliers, partners) → external-party entities
- Named infrastructure → software-component or platform entities
- Named processes or workflows → process entities
- Defined jargon or abbreviations → jargon-business or jargon-tech entities
- Any stated decisions or architectural choices → decision entities

These are STUB entities — they have a name, type, description, and relationships based on what the seed context says. Details will be filled in by subsequent document analysis.

Tag ALL entities with 'seed-context-derived' and 'foundation'.

Be thorough — extract EVERY named concept. The seed context is short and every mention is intentional.

Entity IDs should NOT include the entity type as a prefix. Files are organized into folders by type (e.g., `jargon-business/`, `systems/`, `decisions/`), so `billable-unit` is correct — NOT `jargon-bu` or `jargon-billable-unit`. The ID is the concept name in kebab-case.
"""


def build_seed_extract_prompt(seed_context: str) -> str:
    """Build the prompt for extracting foundation entities from seed context.

    Args:
        seed_context: The full seed context markdown content.

    Returns:
        Complete prompt string.
    """
    from context_blocks.meta_model import format_meta_model_for_prompt

    meta_model = format_meta_model_for_prompt()

    return f"""{meta_model}

---

## Seed Context to Extract From

{seed_context}

---

## Your Task

Extract every named concept from the seed context above as a foundation entity.

For each entity:
- Use the EXACT name from the seed context
- Classify into the correct entity type from the meta-model
- Write a brief description (1-2 sentences) based on what the seed context says
- Add relationships where the seed context explicitly states connections
- Set confidence to 0.7-0.9 (high — this is human-written, reliable information)
- Tag with 'seed-context-derived' and 'foundation'
- For jargon entries in the jargon cheat sheet, create one entity per term

These are foundation entities — they will be enriched by subsequent document analysis. Don't worry about details you don't have yet. The seed context is the truth; capture all of it."""
