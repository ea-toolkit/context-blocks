"""Scan prompt — first pass quick scan to build a document map and reading order.

This prompt scans each document lightly (title, headings, first paragraph)
to classify it and determine the optimal reading order for deep analysis.
"""

from context_blocks.meta_model import format_meta_model_for_prompt


SCAN_SYSTEM_PROMPT = """You are organizing a stack of enterprise documents before reading them deeply. Your job is to quickly scan each document — just the title, headings, and first paragraph — and classify it so we can determine the best reading order.

Think like a smart new joiner who just received a pile of docs: you'd flip through them all quickly first to get the lay of the land before reading any one in depth.

For each document, determine:
1. What TYPE of document is it (architecture overview, API spec, process doc, runbook, glossary, meeting notes, etc.)
2. What SCOPE does it cover (broad/overview vs narrow/specific)
3. What FOLDER it came from (if meaningful — e.g., "confluence" vs "source-code")
4. A one-line SUMMARY of what it appears to be about
5. A suggested READING PRIORITY (1 = read first, 2 = read second, 3 = read last)

Reading order rules:
- Broad overviews and architecture docs should be read FIRST (they provide the frame)
- Glossaries and terminology docs should be read EARLY (they disambiguate everything else)
- Process docs and workflows should be read in the MIDDLE (they connect systems to business)
- Detailed specs, API docs, and runbooks should be read LAST (they make more sense with context)
- Meeting notes and misc docs are lowest priority
"""


def build_scan_prompt(
    documents_summary: list[dict[str, str]],
    seed_context: str,
) -> str:
    """Build the scan prompt for classifying and ordering all documents.

    Args:
        documents_summary: List of dicts with 'filename', 'folder', 'headings', 'first_paragraph'.
        seed_context: The full seed context markdown content.

    Returns:
        The complete prompt string.
    """
    meta_model = format_meta_model_for_prompt()

    docs_section = _format_documents_for_scan(documents_summary)

    return f"""## Seed Context (your domain background)

{seed_context}

---

{meta_model}

---

## Documents to Classify

{docs_section}

---

## Your Task

For each document above, provide:
1. **doc_type** — what kind of document is this (architecture_overview, api_spec, process_doc, glossary, runbook, data_model, decision_record, meeting_notes, configuration, tutorial, other)
2. **scope** — broad (covers multiple systems/concepts) or narrow (focuses on one specific thing)
3. **summary** — one sentence: what this document appears to be about
4. **reading_priority** — 1 (read first — overviews, glossaries), 2 (read second — processes, workflows), 3 (read last — detailed specs, runbooks, meeting notes)
5. **reasoning** — why you assigned this priority

Order your output by reading_priority (1 first, then 2, then 3). Within the same priority, put broader documents before narrower ones."""


def _format_documents_for_scan(documents_summary: list[dict[str, str]]) -> str:
    """Format document summaries for the scan prompt."""
    lines = []
    for i, doc in enumerate(documents_summary, 1):
        lines.append(f"### Document {i}: {doc['filename']}")
        if doc.get('folder'):
            lines.append(f"**Folder:** {doc['folder']}")
        if doc.get('headings'):
            lines.append(f"**Headings:** {doc['headings']}")
        if doc.get('first_paragraph'):
            lines.append(f"**First paragraph:** {doc['first_paragraph'][:500]}")
        lines.append("")
    return "\n".join(lines)
