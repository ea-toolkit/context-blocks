"""Tests for the `cb health-check` command (extract -> eval -> gap report in one)."""

import inspect
import types
from pathlib import Path
from unittest import mock

from typer.testing import CliRunner

from context_blocks.cli import app
from context_blocks.retrieval.evals import CoverageReport, run_coverage_eval

runner = CliRunner()


def _fake_report(clean_pct: float) -> CoverageReport:
    return CoverageReport(
        total_questions=10,
        clean_count=int(clean_pct / 10),
        incomplete_count=0,
        missing_count=10 - int(clean_pct / 10),
        clean_pct=clean_pct,
        incomplete_pct=0.0,
        missing_pct=round(100 - clean_pct, 1),
        per_layer={},
        per_source={},
        per_persona={},
        all_gaps=[],
        results=[],
        total_time_s=1.0,
        total_cost_estimate=0.2,
    )


def _fakes(clean_pct: float):
    async def fake_run_phase1(
        docs_dir, seed_context_path, output_dir, max_documents=None, on_progress=None
    ):
        (Path(output_dir) / "entities").mkdir(parents=True, exist_ok=True)
        return [types.SimpleNamespace(entities=[object(), object()])]

    async def fake_generate_questions(**kwargs):
        return []

    async def fake_generate_persona_questions(**kwargs):
        return []

    async def fake_run_coverage_eval(entity_dir, questions, output_dir, **kwargs):
        return _fake_report(clean_pct)

    def fake_generate_report(eval_json, output_path, block_name=""):
        Path(output_path).write_text("<html>report</html>", encoding="utf-8")
        return {}

    return (
        fake_run_phase1,
        fake_generate_questions,
        fake_generate_persona_questions,
        fake_run_coverage_eval,
        fake_generate_report,
    )


def _run(tmp_path: Path, clean_pct: float, threshold: int):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("# Doc\nSome content.", encoding="utf-8")
    out = tmp_path / "out"

    f = _fakes(clean_pct)
    with mock.patch("context_blocks.pipeline.run_phase1", f[0]), \
         mock.patch("context_blocks.retrieval.evals.generate_questions", f[1]), \
         mock.patch("context_blocks.retrieval.evals.generate_persona_questions", f[2]), \
         mock.patch("context_blocks.retrieval.evals.run_coverage_eval", f[3]), \
         mock.patch("context_blocks.report.generate_report", f[4]):
        result = runner.invoke(
            app,
            [
                "health-check", str(docs),
                "--output", str(out),
                "--threshold", str(threshold),
                "--no-open",
            ],
        )
    return result, out


class TestHealthCheck:
    def test_missing_docs_dir_exits_1(self, tmp_path: Path) -> None:
        result = runner.invoke(app, ["health-check", str(tmp_path / "nope"), "--no-open"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_pass_above_threshold_exits_0(self, tmp_path: Path) -> None:
        result, out = _run(tmp_path, clean_pct=90.0, threshold=70)
        assert result.exit_code == 0, result.output
        assert "PASS" in result.output
        assert (out / "health-check-report.html").exists()

    def test_below_threshold_exits_1(self, tmp_path: Path) -> None:
        result, out = _run(tmp_path, clean_pct=40.0, threshold=70)
        assert result.exit_code == 1
        assert "BELOW THRESHOLD" in result.output

    def test_synthesizes_seed_when_absent(self, tmp_path: Path) -> None:
        result, out = _run(tmp_path, clean_pct=80.0, threshold=70)
        assert result.exit_code == 0, result.output
        assert (out / "_generated-seed.md").exists()

    def test_summary_shows_entities_and_coverage(self, tmp_path: Path) -> None:
        result, _ = _run(tmp_path, clean_pct=85.0, threshold=70)
        assert "Entities:" in result.output
        assert "85" in result.output  # coverage %

    def test_run_coverage_eval_is_coroutine(self) -> None:
        assert inspect.iscoroutinefunction(run_coverage_eval)
