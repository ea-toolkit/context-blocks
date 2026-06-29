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
    test_file = tmp_path / "test.csv"
    test_file.write_text("a,b,c", encoding="utf-8")

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


# ── DOCX ──

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.mark.asyncio
async def test_load_docx_file():
    """Should load a Word document and extract paragraphs."""
    doc = await load_document(FIXTURES / "sample.docx")

    assert doc.filename == "sample.docx"
    assert doc.file_type == "docx"
    assert "claims gateway" in doc.content.lower()
    assert "EDI 837" in doc.content


@pytest.mark.asyncio
async def test_load_docx_extracts_tables():
    """Should extract table content from DOCX."""
    doc = await load_document(FIXTURES / "sample.docx")

    assert "Auto-adjudication" in doc.content
    assert "Specialist Review" in doc.content


@pytest.mark.asyncio
async def test_load_docx_extracts_headings():
    """Should extract heading text from DOCX."""
    doc = await load_document(FIXTURES / "sample.docx")

    assert "Claims Processing Overview" in doc.content
    assert "Routing Rules" in doc.content


# ── PPTX ──


@pytest.mark.asyncio
async def test_load_pptx_file():
    """Should load a PowerPoint and extract slide text."""
    doc = await load_document(FIXTURES / "sample.pptx")

    assert doc.filename == "sample.pptx"
    assert doc.file_type == "pptx"
    assert "claims gateway" in doc.content.lower()


@pytest.mark.asyncio
async def test_load_pptx_has_slide_markers():
    """Should include slide number markers."""
    doc = await load_document(FIXTURES / "sample.pptx")

    assert "## Slide 1" in doc.content
    assert "## Slide 2" in doc.content


@pytest.mark.asyncio
async def test_load_pptx_extracts_tables():
    """Should extract table content from PPTX slides."""
    doc = await load_document(FIXTURES / "sample.pptx")

    assert "Processing Time" in doc.content
    assert "24 hours" in doc.content


@pytest.mark.asyncio
async def test_load_pptx_multiple_slides():
    """Should extract text from all slides."""
    doc = await load_document(FIXTURES / "sample.pptx")

    assert "System Architecture" in doc.content
    assert "Data Flow" in doc.content
    assert "SLA Targets" in doc.content


# ── HTML ──


@pytest.mark.asyncio
async def test_load_html_file():
    """Should load an HTML file and extract body text."""
    doc = await load_document(FIXTURES / "sample.html")

    assert doc.filename == "sample.html"
    assert doc.file_type == "html"
    assert "claims gateway" in doc.content.lower()


@pytest.mark.asyncio
async def test_load_html_strips_nav_footer_script():
    """Should strip nav, footer, header, and script content."""
    doc = await load_document(FIXTURES / "sample.html")

    assert "Home | About | Contact" not in doc.content
    assert "Copyright 2026" not in doc.content
    assert "console.log" not in doc.content
    assert "Site Header" not in doc.content


@pytest.mark.asyncio
async def test_load_html_preserves_body_content():
    """Should preserve meaningful body content."""
    doc = await load_document(FIXTURES / "sample.html")

    assert "Claims Processing" in doc.content
    assert "Adjudication" in doc.content
    assert "specialist review" in doc.content.lower()


@pytest.mark.asyncio
async def test_load_htm_extension():
    """Should support .htm extension."""
    from context_blocks.infrastructure.loaders.base import _extract_html_text

    htm = FIXTURES / "sample.html"
    content = _extract_html_text(htm)
    assert "Claims Processing" in content


# ── Directory loading with mixed formats ──


@pytest.mark.asyncio
async def test_load_directory_mixed_formats(tmp_path: Path):
    """Should load all supported formats from one directory."""
    import shutil

    (tmp_path / "doc.md").write_text("# Markdown doc", encoding="utf-8")
    (tmp_path / "doc.txt").write_text("Plain text doc", encoding="utf-8")
    (tmp_path / "doc.html").write_text("<p>HTML doc</p>", encoding="utf-8")
    shutil.copy(FIXTURES / "sample.docx", tmp_path / "doc.docx")
    shutil.copy(FIXTURES / "sample.pptx", tmp_path / "doc.pptx")

    docs = await load_documents_from_directory(tmp_path)

    types = {d.file_type for d in docs}
    assert types == {"md", "txt", "html", "docx", "pptx"}
