"""Tests for the evals module — question dedup, coverage report, DDC mapping, personas, work items."""

from pathlib import Path

from context_blocks.retrieval.evals import (
    CoverageReport,
    EvalQuestion,
    EvalResult,
    _deduplicate_questions,
    build_coverage_report,
    load_persona_templates,
    load_work_items,
    write_eval_report,
    DDC_TAXONOMY,
)
from context_blocks.retrieval.types import AnswerScore, Gap, RetrievalHop


# ── Fixtures ──

def _make_eval_result(
    question: str = "Test question?",
    score: AnswerScore = AnswerScore.ANSWERABLE,
    source: str = "seed",
    source_file: str = "seed-context",
    layer_hint: str = "structural",
    entities_retrieved: int = 10,
    total_ms: int = 5000,
    gaps: list | None = None,
    hops: list | None = None,
) -> EvalResult:
    return EvalResult(
        question=EvalQuestion(
            question=question,
            source=source,
            source_file=source_file,
            layer_hint=layer_hint,
            topic="test",
        ),
        answer=f"Answer to: {question}",
        score=score,
        ddc_class=DDC_TAXONOMY[score],
        citations=["Entity A", "Entity B"],
        gaps=gaps or [],
        hops=hops or [],
        entities_retrieved=entities_retrieved,
        total_ms=total_ms,
        trace_summary="Entity A → Entity B",
    )


# ── DDC Taxonomy Tests ──

class TestDDCTaxonomy:
    def test_answerable_maps_to_clean(self):
        assert DDC_TAXONOMY[AnswerScore.ANSWERABLE] == "CLEAN"

    def test_partial_maps_to_incomplete(self):
        assert DDC_TAXONOMY[AnswerScore.PARTIAL] == "INCOMPLETE"

    def test_not_answerable_maps_to_missing(self):
        assert DDC_TAXONOMY[AnswerScore.NOT_ANSWERABLE] == "MISSING"


# ── Question Dedup Tests ──

class TestQuestionDedup:
    def test_no_dedup_for_different_questions(self):
        questions = [
            EvalQuestion(question="What is the Rules Engine?", source="seed",
                         source_file="seed-context"),
            EvalQuestion(question="Who owns the Payment Engine?", source="seed",
                         source_file="seed-context"),
        ]
        result = _deduplicate_questions(questions)
        assert len(result) == 2

    def test_dedup_near_identical_questions(self):
        questions = [
            EvalQuestion(question="What is the Rules Engine and how does it work?",
                         source="seed", source_file="seed-context"),
            EvalQuestion(question="What is the Rules Engine and how does it function?",
                         source="doc", source_file="doc1.txt"),
        ]
        result = _deduplicate_questions(questions)
        assert len(result) == 1

    def test_dedup_preserves_first_occurrence(self):
        questions = [
            EvalQuestion(question="What is the claims processing workflow?",
                         source="seed", source_file="seed-context"),
            EvalQuestion(question="What is the claims processing workflow steps?",
                         source="doc", source_file="doc1.txt"),
        ]
        result = _deduplicate_questions(questions)
        assert result[0].source == "seed"

    def test_dedup_empty_list(self):
        assert _deduplicate_questions([]) == []

    def test_dedup_single_question(self):
        questions = [
            EvalQuestion(question="What is X?", source="seed", source_file="seed-context"),
        ]
        result = _deduplicate_questions(questions)
        assert len(result) == 1


# ── Coverage Report Tests ──

class TestCoverageReport:
    def test_correct_counts(self):
        results = [
            _make_eval_result(score=AnswerScore.ANSWERABLE),
            _make_eval_result(score=AnswerScore.ANSWERABLE),
            _make_eval_result(score=AnswerScore.PARTIAL),
            _make_eval_result(score=AnswerScore.NOT_ANSWERABLE),
        ]
        report = build_coverage_report(results, total_time_s=10.0)

        assert report.total_questions == 4
        assert report.clean_count == 2
        assert report.incomplete_count == 1
        assert report.missing_count == 1

    def test_correct_percentages(self):
        results = [
            _make_eval_result(score=AnswerScore.ANSWERABLE),
            _make_eval_result(score=AnswerScore.PARTIAL),
            _make_eval_result(score=AnswerScore.NOT_ANSWERABLE),
            _make_eval_result(score=AnswerScore.NOT_ANSWERABLE),
        ]
        report = build_coverage_report(results, total_time_s=10.0)

        assert report.clean_pct == 25.0
        assert report.incomplete_pct == 25.0
        assert report.missing_pct == 50.0

    def test_per_layer_breakdown(self):
        results = [
            _make_eval_result(score=AnswerScore.ANSWERABLE, layer_hint="structural"),
            _make_eval_result(score=AnswerScore.PARTIAL, layer_hint="structural"),
            _make_eval_result(score=AnswerScore.NOT_ANSWERABLE, layer_hint="behavioral"),
        ]
        report = build_coverage_report(results, total_time_s=10.0)

        assert "structural" in report.per_layer
        assert report.per_layer["structural"]["CLEAN"] == 1
        assert report.per_layer["structural"]["INCOMPLETE"] == 1
        assert "behavioral" in report.per_layer
        assert report.per_layer["behavioral"]["MISSING"] == 1

    def test_per_source_breakdown(self):
        results = [
            _make_eval_result(score=AnswerScore.ANSWERABLE, source="seed"),
            _make_eval_result(score=AnswerScore.PARTIAL, source="doc"),
        ]
        report = build_coverage_report(results, total_time_s=10.0)

        assert report.per_source["seed"]["CLEAN"] == 1
        assert report.per_source["doc"]["INCOMPLETE"] == 1

    def test_empty_results(self):
        report = build_coverage_report([], total_time_s=0)
        assert report.total_questions == 0
        assert report.clean_pct == 0

    def test_gaps_aggregated(self):
        gap = Gap(
            gap_type="orphan_entity", entity_id="e1",
            description="Entity has no relationships",
            suggested_action="Add relationships",
            severity="low", source_question="test",
        )
        results = [
            _make_eval_result(score=AnswerScore.PARTIAL, gaps=[gap]),
            _make_eval_result(score=AnswerScore.PARTIAL, gaps=[gap]),
        ]
        report = build_coverage_report(results, total_time_s=10.0)
        assert len(report.all_gaps) == 2


# ── Report Writer Tests ──

class TestReportWriter:
    def test_report_contains_all_sections(self, tmp_path):
        results = [
            _make_eval_result(score=AnswerScore.ANSWERABLE),
            _make_eval_result(score=AnswerScore.PARTIAL),
            _make_eval_result(score=AnswerScore.NOT_ANSWERABLE),
        ]
        report = build_coverage_report(results, total_time_s=10.0)

        output_path = tmp_path / "eval-report.md"
        write_eval_report(report, output_path)

        content = output_path.read_text()
        assert "# KB Coverage Report" in content
        assert "## Coverage Summary" in content
        assert "## By Question Source" in content
        assert "## By Knowledge Layer" in content
        assert "## Question Results" in content
        assert "## Detailed Results" in content
        assert "CLEAN" in content
        assert "INCOMPLETE" in content
        assert "MISSING" in content

    def test_report_contains_hop_traces(self, tmp_path):
        hop = RetrievalHop(
            entity_id="e1", entity_name="Test Entity", entity_type="system",
            layer="structural", confidence=0.9, hop_number=0,
            matched_by="keyword", fused_score=0.75,
        )
        results = [_make_eval_result(score=AnswerScore.ANSWERABLE, hops=[hop])]
        report = build_coverage_report(results, total_time_s=5.0)

        output_path = tmp_path / "eval-report.md"
        write_eval_report(report, output_path)

        content = output_path.read_text()
        assert "**Retrieval Trace:**" in content
        assert "Test Entity" in content
        assert "keyword" in content

    def test_report_contains_gap_summary(self, tmp_path):
        gap = Gap(
            gap_type="orphan_entity", entity_id="e1",
            description="Test entity has no relationships",
            suggested_action="Add relationships",
            severity="low", source_question="test",
        )
        results = [_make_eval_result(score=AnswerScore.PARTIAL, gaps=[gap])]
        report = build_coverage_report(results, total_time_s=5.0)

        output_path = tmp_path / "eval-report.md"
        write_eval_report(report, output_path)

        content = output_path.read_text()
        assert "## Gap Summary" in content


# ── Persona Template Tests ──

class TestPersonaTemplates:
    def test_default_templates_load(self):
        config = load_persona_templates()
        assert "personas" in config
        personas = config["personas"]
        assert "developer" in personas
        assert "architect" in personas
        assert "product-owner" in personas
        assert "new-joiner" in personas

    def test_each_persona_has_required_fields(self):
        config = load_persona_templates()
        for key, persona in config["personas"].items():
            assert "label" in persona, f"{key} missing label"
            assert "description" in persona, f"{key} missing description"
            assert "checks" in persona, f"{key} missing checks"
            assert len(persona["checks"]) > 0, f"{key} has no checks"

    def test_custom_config_path(self, tmp_path):
        custom = tmp_path / "custom.yaml"
        custom.write_text("""
personas:
  tester:
    label: QA Engineer
    description: Testing perspective
    checks:
      - "Test coverage for critical paths"
      - "Test data management"
""")
        config = load_persona_templates(custom)
        assert "tester" in config["personas"]
        assert len(config["personas"]["tester"]["checks"]) == 2

    def test_missing_config_returns_empty(self, tmp_path):
        config = load_persona_templates(tmp_path / "nonexistent.yaml")
        # Should fall back to default, not crash
        assert "personas" in config


# ── Work Item Parser Tests ──

class TestWorkItemParser:
    def test_loads_markdown_files(self, tmp_path):
        (tmp_path / "ticket-1.md").write_text("# Server returning 500 errors\n\nDetails here.")
        (tmp_path / "ticket-2.md").write_text("# Database connection timeout\n\nMore details.")

        questions = load_work_items(tmp_path)
        assert len(questions) == 2
        assert all(q.source == "work-item" for q in questions)

    def test_loads_txt_files(self, tmp_path):
        (tmp_path / "incident.txt").write_text("Payment batch job failed overnight and needs investigation")

        questions = load_work_items(tmp_path)
        assert len(questions) == 1

    def test_extracts_title_from_heading(self, tmp_path):
        (tmp_path / "ticket.md").write_text("# Claims Gateway returning 504 on batch submissions\n\nDetails.")

        questions = load_work_items(tmp_path)
        assert "Claims Gateway" in questions[0].question

    def test_skips_empty_files(self, tmp_path):
        (tmp_path / "empty.md").write_text("")
        (tmp_path / "real.md").write_text("# Real ticket\n\nContent.")

        questions = load_work_items(tmp_path)
        assert len(questions) == 1

    def test_nonexistent_dir_returns_empty(self, tmp_path):
        questions = load_work_items(tmp_path / "nonexistent")
        assert questions == []

    def test_source_file_is_stem(self, tmp_path):
        (tmp_path / "JIRA-CLP-4521.md").write_text("# Some ticket\n\nContent.")

        questions = load_work_items(tmp_path)
        assert questions[0].source_file == "JIRA-CLP-4521"

    def test_loads_real_synthetic_work_items(self):
        wi_dir = Path("synthetic-domains/healthcare-claims/work-items")
        if wi_dir.exists():
            questions = load_work_items(wi_dir)
            assert len(questions) == 10
            assert all(q.source == "work-item" for q in questions)


# ── Per-Persona Report Tests ──

class TestPerPersonaReport:
    def test_persona_breakdown_in_report(self):
        results = [
            _make_eval_result(score=AnswerScore.ANSWERABLE, source="persona", source_file="developer"),
            _make_eval_result(score=AnswerScore.PARTIAL, source="persona", source_file="developer"),
            _make_eval_result(score=AnswerScore.NOT_ANSWERABLE, source="persona", source_file="architect"),
        ]
        # Tag with persona
        results[0].question.persona = "developer"
        results[1].question.persona = "developer"
        results[2].question.persona = "architect"

        report = build_coverage_report(results, total_time_s=10.0)

        assert "developer" in report.per_persona
        assert report.per_persona["developer"]["CLEAN"] == 1
        assert report.per_persona["developer"]["INCOMPLETE"] == 1
        assert "architect" in report.per_persona
        assert report.per_persona["architect"]["MISSING"] == 1

    def test_persona_section_in_markdown(self, tmp_path):
        results = [
            _make_eval_result(score=AnswerScore.ANSWERABLE, source="persona", source_file="developer"),
        ]
        results[0].question.persona = "developer"

        report = build_coverage_report(results, total_time_s=5.0)
        output_path = tmp_path / "report.md"
        write_eval_report(report, output_path)

        content = output_path.read_text()
        assert "## By Persona" in content
        assert "developer" in content

    def test_no_persona_section_when_no_personas(self, tmp_path):
        results = [_make_eval_result(score=AnswerScore.ANSWERABLE)]
        report = build_coverage_report(results, total_time_s=5.0)

        output_path = tmp_path / "report.md"
        write_eval_report(report, output_path)

        content = output_path.read_text()
        assert "## By Persona" not in content
