"""Pipeline orchestrator — runs Phase 1 (document analysis) end-to-end.

Each document prompt = seed context (fixed)
                     + knowledge summary (fixed size, rewritten each time)
                     + retrieved entities (only ones relevant to current document)
                     + current document

This scales to any number of documents without context window bloat.
"""

from collections.abc import Callable
from pathlib import Path

import structlog

from context_blocks.config import get_settings
from context_blocks.exceptions import ContextBlocksError
from context_blocks.infrastructure.loaders.base import load_documents_from_directory
from context_blocks.models.entity import DocumentExtractionResult
from context_blocks.models.summary import KnowledgeSummary
from context_blocks.models.state import (
    get_unread_documents,
    load_state,
    mark_document_analyzed,
    mark_document_failed,
    mark_document_scanned,
    save_state,
)
from context_blocks.tasks.analyze_document import analyze_document
from context_blocks.tasks.extract_seed_entities import extract_seed_entities
from context_blocks.tasks.scan_documents import scan_documents
from context_blocks.tasks.summarize_knowledge import summarize_knowledge
from context_blocks.tasks.write_entities import save_extraction_json, write_extraction_results

logger = structlog.get_logger(__name__)


async def run_phase1(
    docs_dir: Path,
    seed_context_path: Path,
    output_dir: Path,
    max_documents: int | None = None,
    on_progress: "Callable[[int, int, str], None] | None" = None,
    ontology=None,
) -> list[DocumentExtractionResult]:
    """Run Phase 1: Analyze documents and generate entity files.

    Reads documents sequentially. After each document:
    1. Entities are extracted and written to files
    2. Knowledge summary is rewritten (fixed size — replaces, never grows)
    3. State is saved (crash-safe resume)

    Args:
        docs_dir: Directory containing documents to analyze.
        seed_context_path: Path to the filled seed context markdown file.
        output_dir: Directory to write entity files and reports to.
        max_documents: Optional limit on number of documents to process.
        ontology: Optional custom Ontology for this block. When set, its types drive extraction
            (prompt + validation + directory routing). None → built-in default meta-model.

    Returns:
        List of extraction results, one per document.
    """
    from context_blocks.ontology import set_active_ontology

    # Types drive prompts, entity validation, and directory routing for this run.
    set_active_ontology(ontology)

    logger.info(
        "phase1_start",
        docs_dir=str(docs_dir),
        seed_context_path=str(seed_context_path),
        output_dir=str(output_dir),
        ontology=(ontology.source if ontology is not None else "default"),
    )

    # Validate and load seed context
    from context_blocks.tasks.validate_inputs import validate_seed_context

    seed_context = validate_seed_context(seed_context_path)

    # Load documents
    documents = await load_documents_from_directory(docs_dir)

    if not documents:
        raise ContextBlocksError(f"No supported documents found in {docs_dir}")

    logger.info("phase1_documents_loaded", count=len(documents))

    # Create output directory, initialize trace DB, and load state
    output_dir.mkdir(parents=True, exist_ok=True)

    from context_blocks.infrastructure.llm.trace import init_trace_db
    init_trace_db(output_dir)

    state = load_state(output_dir)

    # Step 0: Extract foundation entities from seed context (runs once)
    if state.total_documents_analyzed == 0 and not state.knowledge_summary:
        logger.info("phase1_seed_extraction_start")
        try:
            seed_result = await extract_seed_entities(seed_context)
            write_extraction_results(seed_result, output_dir)

            entity_ids = [e.id for e in seed_result.entities]
            mark_document_scanned(state, "seed-context", seed_context_path, output_dir=output_dir)
            mark_document_analyzed(state, "seed-context", entity_ids)
            state.total_entities = len(seed_result.entities)
            state.total_documents_analyzed = 1
            save_state(state, output_dir)

            logger.info(
                "phase1_seed_extraction_complete",
                foundation_entities=len(seed_result.entities),
            )
        except Exception as e:
            logger.error("phase1_seed_extraction_failed", error=str(e))
            # Continue without seed entities — not fatal

    # Separate new/changed documents from already-read ones
    to_process, already_read = get_unread_documents(state, documents)
    if already_read:
        logger.info(
            "phase1_skipping_already_read",
            already_read=len(already_read),
            new_or_changed=len(to_process),
        )

    if not to_process:
        logger.info("phase1_nothing_new", message="All documents already analyzed")
        return []

    # Pass 1: Quick scan to classify and determine reading order
    has_existing_scan = any(
        d.status in ("scanned", "analyzed") and d.reading_priority is not None
        for d in state.documents.values()
    )

    if has_existing_scan and already_read:
        # Sort to_process by saved reading priority from previous scan
        priority_map = {
            f: d.reading_priority for f, d in state.documents.items()
            if d.reading_priority is not None
        }
        to_process.sort(key=lambda doc: priority_map.get(doc.filename, 999))

        logger.info(
            "phase1_scan_skipped",
            reason="using sequence from previous run",
            new_documents=len(to_process),
            next_document=to_process[0].filename if to_process else "none",
        )
    else:
        all_documents = to_process + already_read
        logger.info("phase1_scan_start", count=len(all_documents))
        ordered_all = await scan_documents(all_documents, seed_context)
        logger.info("phase1_scan_complete", first_document=ordered_all[0].filename)

        unread_filenames = {doc.filename for doc in to_process}
        to_process = [doc for doc in ordered_all if doc.filename in unread_filenames]

        for i, doc in enumerate(ordered_all):
            mark_document_scanned(state, doc.filename, doc.filepath, reading_priority=i + 1, output_dir=output_dir)
        save_state(state, output_dir)

    # Apply max_documents limit after reordering
    if max_documents:
        to_process = to_process[:max_documents]

    # Skip tiny/stub documents that waste overhead tokens
    from context_blocks.infrastructure.llm.token_utils import estimate_tokens

    settings = get_settings()
    min_tokens = settings.min_doc_tokens
    skipped_tiny = []
    filtered = []
    for doc in to_process:
        doc_tokens = estimate_tokens(doc.content)
        if doc_tokens < min_tokens:
            skipped_tiny.append((doc.filename, doc_tokens))
            mark_document_analyzed(state, doc.filename, [])
        else:
            filtered.append(doc)

    if skipped_tiny:
        logger.info(
            "phase1_skipping_tiny_docs",
            count=len(skipped_tiny),
            threshold=min_tokens,
            docs=[(name, tokens) for name, tokens in skipped_tiny],
        )
        save_state(state, output_dir)

    to_process = filtered

    # Load or initialize knowledge summary
    knowledge_summary: KnowledgeSummary | None = state.knowledge_summary
    all_results: list[DocumentExtractionResult] = []
    total_entities = state.total_entities

    # Circuit breaker: abort after N consecutive failures to avoid burning tokens
    consecutive_failures = 0
    max_consecutive_failures = 3

    for i, document in enumerate(to_process, 1):
        logger.info(
            "phase1_processing",
            document=document.filename,
            progress=f"{i}/{len(to_process)}",
            entities_so_far=total_entities,
        )
        if on_progress:
            on_progress(i, len(to_process), document.filename)

        try:
            # Analyze the document (with summary + retrieved entities)
            result = await analyze_document(
                document=document,
                seed_context=seed_context,
                knowledge_summary=knowledge_summary,
                output_dir=output_dir,
            )

            # Save raw extraction JSON (the expensive artifact — never re-run for format changes)
            save_extraction_json(result, output_dir)

            # Write entity markdown files (cheap render from the JSON above)
            write_extraction_results(result, output_dir)

            # Mark as analyzed BEFORE summary — entities are already saved
            entity_ids = [e.id for e in result.entities]
            mark_document_analyzed(state, document.filename, entity_ids)
            all_results.append(result)
            total_entities += len(result.entities)
            consecutive_failures = 0  # Reset on success

            # Rewrite knowledge summary (non-fatal — stale summary is better than re-extracting)
            try:
                knowledge_summary = await summarize_knowledge(
                    previous_summary=knowledge_summary,
                    extraction_result=result,
                    seed_context=seed_context,
                )
            except Exception as summary_err:
                logger.warning(
                    "phase1_summary_update_failed",
                    document=document.filename,
                    error=str(summary_err),
                )

            # Save state after each document (resume-safe)
            state.knowledge_summary = knowledge_summary
            state.total_entities = total_entities
            state.total_documents_analyzed += 1
            save_state(state, output_dir)

            logger.info(
                "phase1_document_complete",
                document=document.filename,
                entities=len(result.entities),
                questions=len(result.questions),
                total_entities=total_entities,
            )

        except Exception as e:
            consecutive_failures += 1
            remaining_docs = len(to_process) - i

            mark_document_failed(state, document.filename, str(e))
            save_state(state, output_dir)

            logger.error(
                "phase1_document_failed",
                document=document.filename,
                error=str(e),
                consecutive_failures=consecutive_failures,
                remaining_docs=remaining_docs,
            )

            if consecutive_failures >= max_consecutive_failures:
                logger.error(
                    "phase1_circuit_breaker_tripped",
                    consecutive_failures=consecutive_failures,
                    remaining_docs=remaining_docs,
                    message=(
                        f"Aborting: {consecutive_failures} consecutive failures. "
                        f"Skipping {remaining_docs} remaining docs to avoid wasting tokens. "
                        f"Fix the issue and re-run — failed docs will be retried automatically."
                    ),
                )
                break

            continue

    # Write summary report
    _write_summary_report(all_results, knowledge_summary, output_dir)

    # Final state save
    save_state(state, output_dir)

    logger.info(
        "phase1_complete",
        documents_processed=len(all_results),
        documents_failed=len(to_process) - len(all_results),
        documents_skipped=len(already_read),
        total_entities=total_entities,
        output_dir=str(output_dir),
    )

    return all_results


def _write_summary_report(
    results: list[DocumentExtractionResult],
    knowledge_summary: KnowledgeSummary | None,
    output_dir: Path,
) -> None:
    """Write a summary report of the Phase 1 analysis."""
    total_entities = sum(len(r.entities) for r in results)
    all_questions = []
    for r in results:
        all_questions.extend(r.questions)

    lines = [
        "# Context Blocks — Phase 1 Analysis Report",
        "",
        f"**Documents processed:** {len(results)}",
        f"**Total entities extracted:** {total_entities}",
        f"**Unresolved questions:** {len(all_questions)}",
        "",
        "---",
        "",
    ]

    # Include the final knowledge summary
    if knowledge_summary:
        lines.append("## Current Domain Understanding")
        lines.append("")
        lines.append(knowledge_summary.domain_architecture)
        lines.append("")
        if knowledge_summary.key_relationships:
            lines.append("### Key Relationships")
            for rel in knowledge_summary.key_relationships:
                lines.append(f"- {rel}")
            lines.append("")
        if knowledge_summary.open_questions:
            lines.append("### Open Questions")
            for q in knowledge_summary.open_questions:
                lines.append(f"- {q}")
            lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Entities by Document")
    lines.append("")

    for result in results:
        lines.append(f"### {result.source_document}")
        lines.append(f"*{result.document_summary}*")
        lines.append("")
        for entity in result.entities:
            lines.append(
                f"- **{entity.name}** ({entity.entity_type}) "
                f"— {entity.description} [confidence: {entity.confidence:.1f}]"
            )
        lines.append("")

    if all_questions:
        lines.append("---")
        lines.append("")
        lines.append("## All Unresolved Questions")
        lines.append("")
        for q in all_questions:
            lines.append(f"- {q}")
        lines.append("")

    report_path = output_dir / "analysis-report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("summary_report_written", path=str(report_path))
