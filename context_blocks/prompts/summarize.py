"""Summarize prompt — rewrites the accumulated knowledge summary after each document.

The summary is FIXED SIZE — it replaces the previous summary, never appends.
This is how a human updates their mental model: patterns, not notebooks.
"""

SUMMARIZE_SYSTEM_PROMPT = """You are maintaining a running mental model of an enterprise domain as you read documents one by one. After reading each document, you rewrite your understanding as a concise summary.

Rules:
- The summary must be UNDER 1500 words. This is a hard limit.
- Rewrite from scratch each time — don't append to the previous summary.
- Capture PATTERNS and ARCHITECTURE, not individual facts.
- Focus on: how systems connect, why decisions were made, what the domain does.
- Keep track of your top 5 open questions — replace resolved ones with new ones.
- Note any contradictions between what you've read and what the seed context says.
- This summary will be your ONLY memory when reading the next document, so make it count.
"""


def build_summarize_system_prompt(seed_context: str) -> str:
    """Build the cacheable system prompt for summarize calls.

    Combines SUMMARIZE_SYSTEM_PROMPT + seed context so both get cached.

    Args:
        seed_context: The full seed context markdown content.

    Returns:
        Combined system prompt string.
    """
    return f"""{SUMMARIZE_SYSTEM_PROMPT}

---

## Seed Context (for reference)

{seed_context}"""


def build_summarize_prompt(
    previous_summary: str,
    new_document_filename: str,
    new_document_summary: str,
    new_entities: list[str],
    new_questions: list[str],
    new_jargon: list[str],
) -> str:
    """Build the dynamic user prompt for rewriting the knowledge summary.

    The seed context is now in the system prompt (cached). This contains
    only the parts that change per call.

    Args:
        previous_summary: The current knowledge summary (or empty for first doc).
        new_document_filename: Name of the document just processed.
        new_document_summary: Agent's summary of what the document covered.
        new_entities: Entity IDs extracted from the new document.
        new_questions: Questions raised by the new document.
        new_jargon: New jargon terms discovered.

    Returns:
        User prompt string.
    """
    if previous_summary:
        previous_section = f"""## Your Current Understanding (from previous documents)

{previous_summary}"""
    else:
        previous_section = "This is your first document. You have no previous understanding beyond the seed context."

    entities_str = ", ".join(new_entities) if new_entities else "none"
    questions_str = "\n".join(f"- {q}" for q in new_questions) if new_questions else "- none"
    jargon_str = ", ".join(new_jargon) if new_jargon else "none"

    return f"""{previous_section}

---

## What You Just Learned

**Document:** {new_document_filename}
**Summary:** {new_document_summary}
**Entities extracted:** {entities_str}
**New questions:**
{questions_str}
**New jargon:** {jargon_str}

---

## Your Task

Rewrite your complete domain understanding as a single summary. This summary will be your ONLY context (besides seed context) when reading the next document.

Structure your summary as:

### Domain Architecture Understanding
How the systems connect, what the major components are, how data flows.

### Key Relationships and Patterns
Important connections you've noticed across documents.

### Decisions and Reasoning
Why things are the way they are — architectural choices, trade-offs.

### Open Questions (top 5)
The most important things you still don't know.

### Jargon Learned
Terms and their meanings that weren't in the seed context.

Stay under 1500 words. Prioritize understanding over completeness."""
