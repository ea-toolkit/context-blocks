"""Tests for pipeline state management."""

import json
from pathlib import Path

from context_blocks.infrastructure.loaders.base import LoadedDocument
from context_blocks.models.state import (
    PipelineState,
    compute_file_hash,
    get_unread_documents,
    load_state,
    mark_document_analyzed,
    mark_document_scanned,
    save_state,
)


def test_load_state_creates_new_when_missing(tmp_path: Path):
    """Loading state from empty directory creates a fresh state."""
    state = load_state(tmp_path)
    assert state.total_entities == 0
    assert state.total_documents_analyzed == 0
    assert len(state.documents) == 0


def test_save_and_load_roundtrip(tmp_path: Path):
    """State should survive save/load roundtrip."""
    state = PipelineState()
    state.total_entities = 5
    state.total_documents_analyzed = 2

    save_state(state, tmp_path)
    loaded = load_state(tmp_path)

    assert loaded.total_entities == 5
    assert loaded.total_documents_analyzed == 2


def test_corrupted_state_file_handled(tmp_path: Path):
    """Corrupted state file should be backed up and fresh state returned."""
    state_path = tmp_path / ".context-blocks-state.json"
    state_path.write_text("this is not valid json!!!", encoding="utf-8")

    state = load_state(tmp_path)

    assert state.total_entities == 0  # Fresh state
    assert (tmp_path / ".context-blocks-state.json.corrupted").exists()  # Backup created


def test_mark_document_scanned(tmp_path: Path):
    """Marking a document as scanned should update state."""
    state = PipelineState()

    # Create a test file
    test_file = tmp_path / "test.md"
    test_file.write_text("# Test document", encoding="utf-8")

    mark_document_scanned(state, "test.md", test_file, reading_priority=1)

    assert "test.md" in state.documents
    assert state.documents["test.md"].status == "scanned"
    assert state.documents["test.md"].reading_priority == 1


def test_mark_document_analyzed(tmp_path: Path):
    """Marking a document as analyzed should update state with entity IDs."""
    state = PipelineState()

    test_file = tmp_path / "test.md"
    test_file.write_text("# Test", encoding="utf-8")

    mark_document_scanned(state, "test.md", test_file)
    mark_document_analyzed(state, "test.md", ["entity-1", "entity-2"])

    assert state.documents["test.md"].status == "analyzed"
    assert state.documents["test.md"].entities_extracted == ["entity-1", "entity-2"]


def test_get_unread_documents_new_files(tmp_path: Path):
    """New files should be marked for processing."""
    state = PipelineState()

    doc1 = LoadedDocument(
        filename="new.md",
        filepath=tmp_path / "new.md",
        content="new content",
        file_type="md",
        size_bytes=11,
    )
    (tmp_path / "new.md").write_text("new content", encoding="utf-8")

    to_process, already_read = get_unread_documents(state, [doc1])

    assert len(to_process) == 1
    assert len(already_read) == 0


def test_get_unread_documents_skips_analyzed(tmp_path: Path):
    """Already analyzed files with same hash should be skipped."""
    state = PipelineState()

    test_file = tmp_path / "analyzed.md"
    test_file.write_text("content that was analyzed", encoding="utf-8")

    file_hash = compute_file_hash(test_file)

    mark_document_scanned(state, "analyzed.md", test_file)
    mark_document_analyzed(state, "analyzed.md", ["entity-1"])
    # Manually set the hash since mark_document_scanned already computed it
    state.documents["analyzed.md"].file_hash = file_hash

    doc = LoadedDocument(
        filename="analyzed.md",
        filepath=test_file,
        content="content that was analyzed",
        file_type="md",
        size_bytes=25,
    )

    to_process, already_read = get_unread_documents(state, [doc])

    assert len(to_process) == 0
    assert len(already_read) == 1


def test_get_unread_documents_reprocesses_changed(tmp_path: Path):
    """Files with changed content should be re-processed."""
    state = PipelineState()

    test_file = tmp_path / "changed.md"
    test_file.write_text("original content", encoding="utf-8")

    mark_document_scanned(state, "changed.md", test_file)
    mark_document_analyzed(state, "changed.md", ["entity-1"])

    # Now change the file content
    test_file.write_text("updated content", encoding="utf-8")

    doc = LoadedDocument(
        filename="changed.md",
        filepath=test_file,
        content="updated content",
        file_type="md",
        size_bytes=15,
    )

    to_process, already_read = get_unread_documents(state, [doc])

    assert len(to_process) == 1  # Should re-process because hash changed
    assert len(already_read) == 0
