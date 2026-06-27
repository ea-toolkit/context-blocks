"""Analyze Document task — deep reading and entity extraction for a single document.

This is the core task of Context Blocks Phase 1.
Given one document + seed context + knowledge summary + retrieved entities,
produces structured entity extractions.
"""

from pathlib import Path

import structlog

from context_blocks.exceptions import ExtractionError
from context_blocks.infrastructure.llm.gateway import extract_structured
from context_blocks.infrastructure.loaders.base import LoadedDocument
from context_blocks.models.entity import DocumentExtractionResult
from context_blocks.models.summary import KnowledgeSummary
from context_blocks.prompts.analyze import build_analysis_prompt, build_system_prompt
from context_blocks.tasks.retrieve_entities import get_all_entity_ids, retrieve_relevant_entities

logger = structlog.get_logger(__name__)


async def analyze_document(
    document: LoadedDocument,
    seed_context: str,
    knowledge_summary: KnowledgeSummary | None,
    output_dir: Path,
) -> DocumentExtractionResult:
    """Analyze a single document and extract entities.

    Args:
        document: The loaded document to analyze.
        seed_context: The full seed context markdown content.
        knowledge_summary: Fixed-size summary from previous documents (None for first doc).
        output_dir: Output directory for entity retrieval.

    Returns:
        DocumentExtractionResult with extracted entities, questions, and new jargon.

    Raises:
        ExtractionError: If extraction fails for this document.
    """
    docs_read = knowledge_summary.documents_read if knowledge_summary else 0

    logger.info(
        "analyze_start",
        filename=document.filename,
        size_bytes=document.size_bytes,
        documents_processed_so_far=docs_read,
    )

    # Retrieve relevant previously-extracted entities + all existing IDs
    retrieved = retrieve_relevant_entities(document.content, output_dir)
    existing_ids = get_all_entity_ids(output_dir)

    # System prompt: stable across all calls (SYSTEM_PROMPT + seed + meta-model)
    # → cached by Anthropic after first call (90% discount on reads)
    system_prompt = build_system_prompt(seed_context)

    # User prompt: dynamic per document (summary + entity tree + document)
    prompt = build_analysis_prompt(
        document_content=document.content,
        document_filename=document.filename,
        seed_context=seed_context,
        knowledge_summary=knowledge_summary,
        retrieved_entities=retrieved,
        existing_entity_ids=existing_ids if existing_ids else None,
    )

    try:
        result = await extract_structured(
            prompt=prompt,
            response_model=DocumentExtractionResult,
            system_prompt=system_prompt,
            temperature=0.0,
            task_name="analyze",
            document_name=document.filename,
        )

        # Override source_document with actual filename
        result.source_document = document.filename

        logger.info(
            "analyze_complete",
            filename=document.filename,
            entities_extracted=len(result.entities),
            questions_raised=len(result.questions),
            new_jargon=len(result.new_jargon),
        )

        return result

    except Exception as e:
        logger.error(
            "analyze_failed",
            filename=document.filename,
            error=str(e),
        )
        raise ExtractionError(
            f"Failed to analyze document {document.filename}: {e}"
        ) from e
