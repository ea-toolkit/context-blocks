"""Scan Documents task — first pass to classify and order documents before deep analysis.

Reads title, headings, and first paragraph of each document.
Classifies each by type and scope, then determines optimal reading order.
"""

import re

import structlog

from context_blocks.exceptions import ExtractionError
from context_blocks.infrastructure.llm.gateway import extract_structured
from context_blocks.infrastructure.loaders.base import LoadedDocument
from context_blocks.models.scan import ScanResult, ScannedDocument
from context_blocks.prompts.scan import SCAN_SYSTEM_PROMPT, build_scan_prompt

logger = structlog.get_logger(__name__)


def extract_document_preview(document: LoadedDocument) -> dict[str, str]:
    """Extract a quick preview of a document for scanning.

    Reads only the title, headings, and first paragraph — not the full content.

    Args:
        document: The loaded document.

    Returns:
        Dict with filename, folder, headings, and first_paragraph.
    """
    content = document.content

    # Extract folder from filepath (parent directory name)
    folder = ""
    if document.filepath.parent.name and document.filepath.parent.name != ".":
        folder = document.filepath.parent.name

    # Extract headings (markdown ## or # patterns)
    headings = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
    headings_str = " | ".join(headings[:10])  # First 10 headings max

    # Extract first meaningful paragraph (skip empty lines and headings)
    first_paragraph = ""
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---") and len(line) > 20:
            first_paragraph = line[:500]
            break

    return {
        "filename": document.filename,
        "folder": folder,
        "headings": headings_str,
        "first_paragraph": first_paragraph,
    }


async def scan_documents(
    documents: list[LoadedDocument],
    seed_context: str,
) -> list[LoadedDocument]:
    """Scan all documents and return them in optimal reading order.

    First pass: quick scan of titles/headings/first paragraphs.
    Classifies each document and determines reading priority.
    Returns documents reordered for deep analysis.

    Args:
        documents: List of loaded documents in original order.
        seed_context: The full seed context markdown content.

    Returns:
        Same documents reordered by reading priority (overviews first, specs last).
    """
    logger.info("scan_start", document_count=len(documents))

    # Extract previews for all documents
    previews = [extract_document_preview(doc) for doc in documents]

    # Build and send scan prompt
    prompt = build_scan_prompt(previews, seed_context)

    try:
        scan_result = await extract_structured(
            prompt=prompt,
            response_model=ScanResult,
            system_prompt=SCAN_SYSTEM_PROMPT,
            temperature=0.0,
            task_name="scan",
            document_name="all_documents",
        )

        logger.info(
            "scan_complete",
            total=scan_result.total_documents,
            summary=scan_result.reading_order_summary,
        )

        # Log the scan results
        for scanned in scan_result.documents:
            logger.debug(
                "scan_document_classified",
                filename=scanned.filename,
                doc_type=scanned.doc_type.value,
                scope=scanned.scope.value,
                priority=scanned.reading_priority,
                summary=scanned.summary,
            )

        # Reorder documents based on scan results
        return _reorder_documents(documents, scan_result)

    except Exception as e:
        logger.warning(
            "scan_failed_fallback_to_original_order",
            error=str(e),
        )
        # If scanning fails, fall back to original order — don't crash the pipeline
        return documents


def _reorder_documents(
    documents: list[LoadedDocument],
    scan_result: ScanResult,
) -> list[LoadedDocument]:
    """Reorder documents based on scan results.

    Args:
        documents: Original document list.
        scan_result: Scan classification results with reading priorities.

    Returns:
        Documents reordered by reading priority.
    """
    # Build a filename → document map
    doc_map = {doc.filename: doc for doc in documents}

    # Build ordered list from scan results
    ordered = []
    seen = set()

    for scanned in sorted(scan_result.documents, key=lambda d: (d.reading_priority, d.scope.value)):
        if scanned.filename in doc_map and scanned.filename not in seen:
            ordered.append(doc_map[scanned.filename])
            seen.add(scanned.filename)

    # Add any documents that weren't in the scan results (shouldn't happen, but safety)
    for doc in documents:
        if doc.filename not in seen:
            ordered.append(doc)
            logger.warning("scan_document_not_classified", filename=doc.filename)

    logger.info(
        "documents_reordered",
        original_first=documents[0].filename if documents else "none",
        reordered_first=ordered[0].filename if ordered else "none",
    )

    return ordered
