"""Pipeline state — tracks what has been read, when, and what was extracted.

Persisted as a JSON file in the output directory so the pipeline can resume,
skip already-read files, and detect new/changed documents.
"""

from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from context_blocks.models.summary import KnowledgeSummary


class DocumentReadState(BaseModel):
    """Track the read state of a single document."""

    filename: str
    filepath: str  # relative to output directory
    file_hash: str  # MD5 hash to detect content changes
    status: str = Field(
        default="unread",
        description="unread, scanned, analyzed, failed"
    )
    scanned_at: datetime | None = None
    analyzed_at: datetime | None = None
    entities_extracted: list[str] = Field(
        default_factory=list,
        description="Entity IDs extracted from this document"
    )
    reading_priority: int | None = None
    error: str | None = None


class PipelineState(BaseModel):
    """Full pipeline state — persisted between runs."""

    version: str = "1.0"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_run_at: datetime | None = None
    documents: dict[str, DocumentReadState] = Field(
        default_factory=dict,
        description="Map of filename → read state"
    )
    knowledge_summary: KnowledgeSummary | None = Field(
        default=None,
        description="Fixed-size knowledge summary — rewritten after each document"
    )
    total_entities: int = 0
    total_documents_analyzed: int = 0


def load_state(output_dir: Path) -> PipelineState:
    """Load pipeline state from disk, or create new if not found.

    Handles corrupted state files gracefully — backs up and starts fresh.
    Migrates absolute paths to relative on load (backwards compat).
    """
    import json
    import shutil

    import structlog

    logger = structlog.get_logger(__name__)
    state_path = output_dir / ".context-blocks-state.json"

    if state_path.exists():
        try:
            data = json.loads(state_path.read_text(encoding="utf-8"))
            state = PipelineState.model_validate(data)
            _migrate_absolute_paths(state, output_dir, logger)
            return state
        except Exception as e:
            backup_path = state_path.with_suffix(".json.corrupted")
            shutil.copy2(state_path, backup_path)
            logger.warning(
                "state_file_corrupted",
                error=str(e),
                backup=str(backup_path),
            )
            return PipelineState()

    return PipelineState()


def _migrate_absolute_paths(
    state: PipelineState, output_dir: Path, logger: object
) -> None:
    """Convert any absolute filepaths to relative. Idempotent."""
    migrated = 0
    for doc_state in state.documents.values():
        p = Path(doc_state.filepath)
        if p.is_absolute():
            try:
                doc_state.filepath = str(p.relative_to(output_dir))
            except ValueError:
                doc_state.filepath = p.name
            migrated += 1
    if migrated and hasattr(logger, "info"):
        logger.info("state_migrated_absolute_paths", count=migrated)  # type: ignore[union-attr]


def save_state(state: PipelineState, output_dir: Path) -> None:
    """Persist pipeline state to disk."""
    import json

    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / ".context-blocks-state.json"

    state.last_run_at = datetime.now(timezone.utc)

    state_path.write_text(
        json.dumps(state.model_dump(), indent=2, default=str),
        encoding="utf-8",
    )


def compute_file_hash(filepath: Path) -> str:
    """Compute MD5 hash of a file for change detection."""
    import hashlib

    return hashlib.md5(filepath.read_bytes()).hexdigest()


def get_unread_documents(
    state: PipelineState,
    documents: list,
) -> tuple[list, list]:
    """Separate documents into new/changed and already-read.

    Args:
        state: Current pipeline state.
        documents: All loaded documents.

    Returns:
        Tuple of (documents_to_process, documents_already_read).
    """
    to_process = []
    already_read = []

    for doc in documents:
        file_hash = compute_file_hash(doc.filepath)
        existing = state.documents.get(doc.filename)

        if existing is None:
            # New document — never seen before
            to_process.append(doc)
        elif existing.file_hash != file_hash:
            # Content changed since last read — re-process
            to_process.append(doc)
        elif existing.status == "analyzed":
            # Already successfully analyzed and content unchanged
            already_read.append(doc)
        elif existing.status == "failed":
            # Previously failed — retry
            to_process.append(doc)
        else:
            # Scanned but not analyzed, or other state — process
            to_process.append(doc)

    return to_process, already_read


def mark_document_scanned(
    state: PipelineState,
    filename: str,
    filepath: Path,
    reading_priority: int | None = None,
    output_dir: Path | None = None,
) -> None:
    """Mark a document as scanned (Pass 1 complete)."""
    from datetime import datetime, timezone

    file_hash = compute_file_hash(filepath)

    stored_path = str(filepath)
    if output_dir and filepath.is_absolute():
        try:
            stored_path = str(filepath.relative_to(output_dir))
        except ValueError:
            stored_path = filepath.name

    state.documents[filename] = DocumentReadState(
        filename=filename,
        filepath=stored_path,
        file_hash=file_hash,
        status="scanned",
        scanned_at=datetime.now(timezone.utc),
        reading_priority=reading_priority,
    )


def mark_document_analyzed(
    state: PipelineState,
    filename: str,
    entity_ids: list[str],
) -> None:
    """Mark a document as fully analyzed (Pass 2 complete)."""
    from datetime import datetime, timezone

    if filename in state.documents:
        doc_state = state.documents[filename]
        doc_state.status = "analyzed"
        doc_state.analyzed_at = datetime.now(timezone.utc)
        doc_state.entities_extracted = entity_ids
        doc_state.error = None


def mark_document_failed(
    state: PipelineState,
    filename: str,
    error: str,
) -> None:
    """Mark a document as failed."""
    if filename in state.documents:
        state.documents[filename].status = "failed"
        state.documents[filename].error = error
