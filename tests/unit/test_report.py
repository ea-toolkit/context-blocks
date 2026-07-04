"""Tests for the gap report HTML generation."""

import json
from pathlib import Path

import pytest

from context_blocks.report import (
    ReportData,
    generate_html,
    generate_report,
    load_eval_results,
)


# ── Fixtures ──

def _make_eval_item(
    question: str = "Test question?",
    ddc_class: str = "CLEAN",
    source: str = "seed",
    persona: str = "",
    layer_hint: str = "structural",
    entities_retrieved: int = 10,
    total_ms: int = 5000,
    gaps: list | None = None,
) -> dict:
    return {
        "question": question,
        "source": source,
        "source_file": persona or "seed-context",
        "layer_hint": layer_hint,
        "topic": "test",
        "persona": persona,
        "score": "answerable" if ddc_class == "CLEAN" else "partial" if ddc_class == "INCOMPLETE" else "not_answerable",
        "ddc_class": ddc_class,
        "answer": f"Answer to: {question}",
        "citations": ["entity-1"],
        "entities_retrieved": entities_retrieved,
        "total_ms": total_ms,
        "trace_summary": "entity-1 (system, vector, conf=90%)",
        "hops": [],
        "gaps": gaps or [],
    }


def _make_eval_json(tmp_path: Path, items: list[dict]) -> Path:
    eval_json = tmp_path / "eval-results.json"
    eval_json.write_text(json.dumps(items), encoding="utf-8")
    return eval_json


# ── load_eval_results ──

class TestLoadEvalResults:
    def test_counts_classes(self, tmp_path: Path) -> None:
        items = [
            _make_eval_item(ddc_class="CLEAN"),
            _make_eval_item(ddc_class="CLEAN"),
            _make_eval_item(ddc_class="INCOMPLETE"),
            _make_eval_item(ddc_class="MISSING"),
        ]
        rd = load_eval_results(_make_eval_json(tmp_path, items))
        assert rd.total == 4
        assert rd.clean == 2
        assert rd.incomplete == 1
        assert rd.missing == 1

    def test_per_persona_breakdown(self, tmp_path: Path) -> None:
        items = [
            _make_eval_item(ddc_class="CLEAN", source="persona", persona="developer"),
            _make_eval_item(ddc_class="INCOMPLETE", source="persona", persona="developer"),
            _make_eval_item(ddc_class="MISSING", source="persona", persona="architect"),
        ]
        rd = load_eval_results(_make_eval_json(tmp_path, items))
        assert "developer" in rd.per_persona
        assert rd.per_persona["developer"]["CLEAN"] == 1
        assert rd.per_persona["developer"]["INCOMPLETE"] == 1
        assert rd.per_persona["developer"]["total"] == 2
        assert "architect" in rd.per_persona
        assert rd.per_persona["architect"]["MISSING"] == 1

    def test_per_layer_breakdown(self, tmp_path: Path) -> None:
        items = [
            _make_eval_item(ddc_class="CLEAN", layer_hint="structural"),
            _make_eval_item(ddc_class="INCOMPLETE", layer_hint="structural"),
            _make_eval_item(ddc_class="CLEAN", layer_hint="behavioral"),
        ]
        rd = load_eval_results(_make_eval_json(tmp_path, items))
        assert rd.per_layer["structural"]["CLEAN"] == 1
        assert rd.per_layer["structural"]["INCOMPLETE"] == 1
        assert rd.per_layer["behavioral"]["CLEAN"] == 1

    def test_per_source_breakdown(self, tmp_path: Path) -> None:
        items = [
            _make_eval_item(ddc_class="CLEAN", source="seed"),
            _make_eval_item(ddc_class="MISSING", source="persona", persona="dev"),
        ]
        rd = load_eval_results(_make_eval_json(tmp_path, items))
        assert rd.per_source["seed"]["CLEAN"] == 1
        assert rd.per_source["persona"]["MISSING"] == 1

    def test_deduplicates_gaps(self, tmp_path: Path) -> None:
        gap = {"gap_type": "missing_entity", "entity_id": "foo", "description": "Missing foo entity", "severity": "high"}
        items = [
            _make_eval_item(gaps=[gap]),
            _make_eval_item(gaps=[gap]),
        ]
        rd = load_eval_results(_make_eval_json(tmp_path, items))
        assert len(rd.gaps) == 1

    def test_empty_results(self, tmp_path: Path) -> None:
        rd = load_eval_results(_make_eval_json(tmp_path, []))
        assert rd.total == 0
        assert rd.clean == 0
        assert rd.incomplete == 0
        assert rd.missing == 0


# ── generate_html ──

class TestGenerateHtml:
    def test_returns_valid_html(self) -> None:
        rd = ReportData(total=3, clean=2, incomplete=1, missing=0)
        html = generate_html(rd, "test-block")
        assert html.startswith("<!DOCTYPE html>")
        assert "</html>" in html

    def test_contains_block_name(self) -> None:
        rd = ReportData(total=1, clean=1)
        html = generate_html(rd, "my-project")
        assert "my-project" in html

    def test_contains_score_cards(self) -> None:
        rd = ReportData(total=10, clean=6, incomplete=3, missing=1)
        html = generate_html(rd)
        assert "60%" in html  # clean pct
        assert "30%" in html  # incomplete pct
        assert "10%" in html  # missing pct

    def test_contains_persona_rows(self) -> None:
        rd = ReportData(
            total=2,
            clean=1,
            incomplete=1,
            per_persona={"developer": {"CLEAN": 1, "INCOMPLETE": 1, "MISSING": 0, "total": 2}},
        )
        html = generate_html(rd)
        assert "developer" in html
        assert "50%" in html

    def test_contains_gap_items(self) -> None:
        rd = ReportData(
            total=1,
            missing=1,
            gaps=[{"gap_type": "missing_entity", "severity": "high", "description": "Entity X is missing"}],
        )
        html = generate_html(rd)
        assert "missing entity" in html
        assert "Entity X is missing" in html
        assert "severity-high" in html

    def test_contains_top_unanswered(self) -> None:
        rd = ReportData(
            total=2,
            clean=1,
            missing=1,
            questions=[
                _make_eval_item(question="Answerable question?", ddc_class="CLEAN"),
                _make_eval_item(question="Unanswerable question?", ddc_class="MISSING"),
            ],
        )
        html = generate_html(rd)
        assert "Unanswerable question?" in html

    def test_escapes_html_in_questions(self) -> None:
        rd = ReportData(
            total=1,
            clean=1,
            questions=[_make_eval_item(question="What about <script>alert('xss')</script>?")],
        )
        html = generate_html(rd)
        assert "<script>alert" not in html
        assert "&lt;script&gt;" in html

    def test_dark_and_light_mode(self) -> None:
        rd = ReportData(total=1, clean=1)
        html = generate_html(rd)
        assert 'data-theme="dark"' in html
        assert '[data-theme="light"]' in html
        assert "toggleTheme" in html


# ── generate_report (end-to-end) ──

class TestGenerateReport:
    def test_writes_html_file(self, tmp_path: Path) -> None:
        items = [
            _make_eval_item(ddc_class="CLEAN", source="persona", persona="developer"),
            _make_eval_item(ddc_class="INCOMPLETE", source="persona", persona="architect"),
            _make_eval_item(ddc_class="MISSING", source="seed"),
        ]
        _make_eval_json(tmp_path, items)
        output_path = tmp_path / "gap-report.html"

        stats = generate_report(tmp_path / "eval-results.json", output_path, "test-block")

        assert output_path.exists()
        assert stats["total"] == 3
        assert stats["clean"] == 1
        assert stats["incomplete"] == 1
        assert stats["missing"] == 1
        assert stats["personas"] == 2
        assert stats["output"] == str(output_path)

        html = output_path.read_text(encoding="utf-8")
        assert "test-block" in html
        assert "<!DOCTYPE html>" in html

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        items = [_make_eval_item()]
        _make_eval_json(tmp_path, items)
        output_path = tmp_path / "nested" / "dir" / "report.html"

        generate_report(tmp_path / "eval-results.json", output_path)

        assert output_path.exists()

    def test_real_eval_file(self) -> None:
        """Smoke test against the shipped healthcare-claims eval data."""
        eval_json = Path(__file__).parent.parent.parent / "synthetic-domains" / "healthcare-claims" / "output" / "eval-results.json"
        if not eval_json.exists():
            pytest.skip("Healthcare claims eval data not available")

        rd = load_eval_results(eval_json)
        assert rd.total > 0
        assert rd.clean + rd.incomplete + rd.missing == rd.total

        html = generate_html(rd, "healthcare-claims")
        assert "<!DOCTYPE html>" in html
        assert "healthcare-claims" in html
