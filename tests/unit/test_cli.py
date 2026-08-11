"""CLI command tests — focused on `cb mcp` block resolution."""

from pathlib import Path

import pytest
import typer

import context_blocks.mcp_server as mcp_mod
from context_blocks.cli import mcp_serve


@pytest.fixture()
def captured_run(monkeypatch):
    """Capture what mcp_serve hands run_server, without starting the server."""
    calls: dict = {}
    monkeypatch.setattr(mcp_mod, "run_server", lambda **kw: calls.update(called=True, **kw))
    return calls


def test_mcp_output_flag_serves_that_block(tmp_path: Path, captured_run) -> None:
    # Regression: `cb mcp --output <dir>` (no --block) must serve that block,
    # not silently fall through to the "all blocks" path.
    (tmp_path / "entities").mkdir()
    mcp_serve(output=tmp_path, block=None, transport=None, host=None, port=None)
    assert captured_run["output_dir"] == str(tmp_path)


def test_mcp_no_flags_serves_all_blocks(captured_run) -> None:
    mcp_serve(output=None, block=None, transport=None, host=None, port=None)
    assert captured_run.get("called") is True
    assert "output_dir" not in captured_run


def test_mcp_output_missing_entities_errors(tmp_path: Path, captured_run) -> None:
    with pytest.raises(typer.Exit):
        mcp_serve(output=tmp_path / "nope", block=None, transport=None, host=None, port=None)
    assert "called" not in captured_run  # never reached run_server
