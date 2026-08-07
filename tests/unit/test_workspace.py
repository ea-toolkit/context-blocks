"""Tests for workspace-root resolution (public/private toggle)."""

from pathlib import Path

import pytest

from context_blocks.blocks import find_repo_root, resolve_workspace_root

_ENV = (
    "CB_PROJECT_ROOT",
    "CB_WORKSPACE",
    "CB_WORKSPACE_PUBLIC",
    "CB_WORKSPACE_PRIVATE",
)


@pytest.fixture()
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path.resolve()
    (root / "pyproject.toml").write_text("[project]\n")
    monkeypatch.chdir(root)
    for var in _ENV:
        monkeypatch.delenv(var, raising=False)
    return root


def test_explicit_project_root_overrides_workspace(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CB_PROJECT_ROOT", "/tmp/explicit")
    monkeypatch.setenv("CB_WORKSPACE", "public")
    assert resolve_workspace_root() == Path("/tmp/explicit")


def test_public_workspace_default_path(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CB_WORKSPACE", "public")
    assert resolve_workspace_root() == repo / "synthetic-domains"


def test_private_workspace_default_path(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CB_WORKSPACE", "private")
    assert resolve_workspace_root() == repo / ".private" / "blocks"


def test_custom_workspace_path(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CB_WORKSPACE", "public")
    monkeypatch.setenv("CB_WORKSPACE_PUBLIC", "demos")
    assert resolve_workspace_root() == repo / "demos"


def test_absolute_workspace_path_respected(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CB_WORKSPACE", "private")
    monkeypatch.setenv("CB_WORKSPACE_PRIVATE", "/data/blocks")
    assert resolve_workspace_root() == Path("/data/blocks")


def test_no_env_falls_back_to_discovery(repo: Path) -> None:
    (repo / "blocks.yaml").write_text("{}\n")
    assert resolve_workspace_root() == repo


def test_unknown_workspace_falls_back_to_discovery(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CB_WORKSPACE", "bogus")
    (repo / "blocks.yaml").write_text("{}\n")
    assert resolve_workspace_root() == repo


def test_workspace_case_insensitive(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CB_WORKSPACE", "  Private ")
    assert resolve_workspace_root() == repo / ".private" / "blocks"


def test_find_repo_root_by_git_marker(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    (root / ".git").mkdir()
    nested = root / "a" / "b"
    nested.mkdir(parents=True)
    assert find_repo_root(nested) == root
