"""Tests for document loaders."""

import pytest
from pathlib import Path

from context_blocks.infrastructure.loaders.base import load_document, load_documents_from_directory
from context_blocks.exceptions import DocumentLoadError


@pytest.mark.asyncio
async def test_load_markdown_file(tmp_path: Path):
    """Should load a markdown file successfully."""
    test_file = tmp_path / "test.md"
    test_file.write_text("# Hello\n\nThis is a test.", encoding="utf-8")

    doc = await load_document(test_file)

    assert doc.filename == "test.md"
    assert doc.content == "# Hello\n\nThis is a test."
    assert doc.file_type == "md"


@pytest.mark.asyncio
async def test_load_text_file(tmp_path: Path):
    """Should load a plain text file successfully."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Just some text.", encoding="utf-8")

    doc = await load_document(test_file)

    assert doc.filename == "test.txt"
    assert doc.file_type == "txt"


@pytest.mark.asyncio
async def test_load_missing_file(tmp_path: Path):
    """Should raise DocumentLoadError for missing files."""
    with pytest.raises(DocumentLoadError, match="File not found"):
        await load_document(tmp_path / "nonexistent.md")


@pytest.mark.asyncio
async def test_load_empty_file(tmp_path: Path):
    """Should raise DocumentLoadError for empty files."""
    test_file = tmp_path / "empty.md"
    test_file.write_text("", encoding="utf-8")

    with pytest.raises(DocumentLoadError, match="empty"):
        await load_document(test_file)


@pytest.mark.asyncio
async def test_load_unsupported_type(tmp_path: Path):
    """Should raise DocumentLoadError for unsupported file types."""
    test_file = tmp_path / "test.docx"
    test_file.write_text("content", encoding="utf-8")

    with pytest.raises(DocumentLoadError, match="Unsupported"):
        await load_document(test_file)


@pytest.mark.asyncio
async def test_load_directory_recursive(tmp_path: Path):
    """Should load documents from nested subdirectories."""
    # Create nested structure
    sub_dir = tmp_path / "confluence"
    sub_dir.mkdir()
    (sub_dir / "overview.md").write_text("# Overview", encoding="utf-8")
    (tmp_path / "root.md").write_text("# Root doc", encoding="utf-8")

    docs = await load_documents_from_directory(tmp_path)

    assert len(docs) == 2
    filenames = {d.filename for d in docs}
    assert "overview.md" in filenames
    assert "root.md" in filenames


@pytest.mark.asyncio
async def test_load_directory_skips_dotfiles(tmp_path: Path):
    """Should skip hidden/dot files."""
    (tmp_path / ".hidden.md").write_text("# Hidden", encoding="utf-8")
    (tmp_path / "visible.md").write_text("# Visible", encoding="utf-8")

    docs = await load_documents_from_directory(tmp_path)

    assert len(docs) == 1
    assert docs[0].filename == "visible.md"


@pytest.mark.asyncio
async def test_load_directory_skips_empty_files(tmp_path: Path):
    """Should skip empty files without crashing."""
    (tmp_path / "empty.md").write_text("", encoding="utf-8")
    (tmp_path / "good.md").write_text("# Good content", encoding="utf-8")

    docs = await load_documents_from_directory(tmp_path)

    assert len(docs) == 1
    assert docs[0].filename == "good.md"
