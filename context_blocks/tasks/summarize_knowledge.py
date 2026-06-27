"""Summarize Knowledge task — rewrites the knowledge summary after each document.

Called after each document analysis. Produces a fixed-size summary
that replaces the previous one. The agent's mental model, not a notebook.
"""

import structlog

from context_blocks.infrastructure.llm.gateway import extract_structured
from context_blocks.models.entity import DocumentExtractionResult
from context_blocks.models.summary import KnowledgeSummary
from context_blocks.prompts.summarize import build_summarize_prompt, build_summarize_system_prompt

logger = structlog.get_logger(__name__)


async def summarize_knowledge(
    previous_summary: KnowledgeSummary | None,
    extraction_result: DocumentExtractionResult,
    seed_context: str,
) -> KnowledgeSummary:
    """Rewrite the knowledge summary after processing a document.

    Args:
        previous_summary: Current summary (None for first document).
        extraction_result: What was just extracted from the latest document.
        seed_context: The seed context for reference.

    Returns:
        New KnowledgeSummary replacing the previous one.
    """
    previous_text = previous_summary.to_prompt_text() if previous_summary else ""
    prev_docs = previous_summary.documents_read if previous_summary else 0
    prev_entities = previous_summary.entities_discovered_count if previous_summary else 0

    # System prompt: stable (instructions + seed context) → cached
    system_prompt = build_summarize_system_prompt(seed_context)

    # User prompt: dynamic (previous summary + new doc info)
    prompt = build_summarize_prompt(
        previous_summary=previous_text,
        new_document_filename=extraction_result.source_document,
        new_document_summary=extraction_result.document_summary,
        new_entities=[e.id for e in extraction_result.entities],
        new_questions=extraction_result.questions,
        new_jargon=extraction_result.new_jargon,
    )

    try:
        summary = await extract_structured(
            prompt=prompt,
            response_model=KnowledgeSummary,
            system_prompt=system_prompt,
            temperature=0.0,
            task_name="summarize",
            document_name=extraction_result.source_document,
        )

        # Update counters
        summary.documents_read = prev_docs + 1
        summary.entities_discovered_count = prev_entities + len(extraction_result.entities)

        logger.info(
            "knowledge_summary_updated",
            documents_read=summary.documents_read,
            entities_total=summary.entities_discovered_count,
            open_questions=len(summary.open_questions),
        )

        return summary

    except Exception as e:
        logger.error("knowledge_summary_failed", error=str(e))

        # Fallback: keep previous summary with updated counters
        if previous_summary:
            previous_summary.documents_read = prev_docs + 1
            previous_summary.entities_discovered_count = prev_entities + len(extraction_result.entities)
            return previous_summary

        # No previous summary and summarization failed — create minimal one
        return KnowledgeSummary(
            domain_architecture=f"Read {extraction_result.source_document}: {extraction_result.document_summary}",
            key_relationships="Still building understanding.",
            decisions_and_reasoning="Still building understanding.",
            open_questions=extraction_result.questions[:5],
            documents_read=1,
            entities_discovered_count=len(extraction_result.entities),
        )
