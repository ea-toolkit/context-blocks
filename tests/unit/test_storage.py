"""Tests for block artifact storage (the persistence boundary)."""

from pathlib import Path

from context_blocks import storage


def test_is_allowed_artifact() -> None:
    assert storage.is_allowed_artifact("architecture.drawio")
    assert storage.is_allowed_artifact("flow.BPMN")  # case-insensitive
    assert storage.is_allowed_artifact("photo.png")
    assert not storage.is_allowed_artifact("notes.md")
    assert not storage.is_allowed_artifact("script.py")


def test_safe_filename_strips_paths() -> None:
    assert storage.safe_filename("../../etc/passwd") == "passwd"
    assert storage.safe_filename("a/b/c.png") == "c.png"
    assert storage.safe_filename("clean.xml") == "clean.xml"


def test_guess_content_type() -> None:
    assert storage.guess_content_type("x.bpmn") == "application/xml"
    assert storage.guess_content_type("x.drawio") == "application/xml"
    assert storage.guess_content_type("x.svg") == "image/svg+xml"
    assert storage.guess_content_type("x.png") == "image/png"
    assert storage.guess_content_type("x.unknown") == "application/octet-stream"


def test_save_and_read_artifact(tmp_path: Path) -> None:
    info = storage.save_artifact(tmp_path, "diagram.drawio", b"<mxfile></mxfile>")
    assert info.filename == "diagram.drawio"
    assert info.path == "artifacts/diagram.drawio"
    assert info.content_type == "application/xml"
    assert info.size == len(b"<mxfile></mxfile>")
    assert (tmp_path / "artifacts" / "diagram.drawio").exists()

    result = storage.read_artifact(tmp_path, "diagram.drawio")
    assert result is not None
    data, content_type = result
    assert data == b"<mxfile></mxfile>"
    assert content_type == "application/xml"


def test_save_artifact_sanitizes_traversal(tmp_path: Path) -> None:
    info = storage.save_artifact(tmp_path, "../../evil.png", b"x")
    assert info.filename == "evil.png"
    assert (tmp_path / "artifacts" / "evil.png").exists()
    assert not (tmp_path.parent / "evil.png").exists()


def test_read_missing_artifact_returns_none(tmp_path: Path) -> None:
    assert storage.read_artifact(tmp_path, "nope.png") is None


def test_list_artifacts_empty_then_populated(tmp_path: Path) -> None:
    assert storage.list_artifacts(tmp_path) == []
    storage.save_artifact(tmp_path, "a.png", b"a")
    storage.save_artifact(tmp_path, "b.bpmn", b"<x/>")
    names = {a.filename for a in storage.list_artifacts(tmp_path)}
    assert names == {"a.png", "b.bpmn"}


def test_save_overwrites_by_name(tmp_path: Path) -> None:
    storage.save_artifact(tmp_path, "a.png", b"one")
    storage.save_artifact(tmp_path, "a.png", b"two")
    result = storage.read_artifact(tmp_path, "a.png")
    assert result is not None and result[0] == b"two"
    assert len(storage.list_artifacts(tmp_path)) == 1
