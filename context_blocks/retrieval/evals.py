"""Evals — question generation + coverage scoring for Context Blocks KBs.

Four question sources:
  1. Seed context → broad domain questions (tests retrieval + synthesis)
  2. Source docs → specific questions per doc (tests extraction coverage + retrieval)
  3. Persona templates → structural completeness checks (tests KB breadth per role)
  4. Work items → real demands from tickets/incidents (tests true domain coverage = DDC)

Coverage maps to DDC taxonomy:
  ANSWERABLE  → CLEAN      (KB fully covers this)
  PARTIAL     → INCOMPLETE  (KB partially covers, key info missing)
  NOT_ANSWERABLE → MISSING  (KB doesn't cover this at all)
"""
import json
import os
import random
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import structlog

from context_blocks.retrieval.types import AnswerScore, Gap, RetrievalHop, RetrievalResult

logger = structlog.get_logger(__name__)

DDC_TAXONOMY = {
    AnswerScore.ANSWERABLE: "CLEAN",
    AnswerScore.PARTIAL: "INCOMPLETE",
    AnswerScore.NOT_ANSWERABLE: "MISSING",
}

# ── Data Types ──

@dataclass
class EvalQuestion:
    """A generated eval question with metadata."""
    question: str
    source: str  # 'seed' | 'doc' | 'persona' | 'work-item'
    source_file: str  # filename, 'seed-context', persona name, or ticket ID
    layer_hint: str = ""  # expected layer if known
    topic: str = ""  # brief topic label
    persona: str = ""  # persona name if source='persona'


@dataclass
class EvalResult:
    """Result of evaluating one question against the KB."""
    question: EvalQuestion
    answer: str
    score: AnswerScore
    ddc_class: str  # CLEAN | INCOMPLETE | MISSING
    citations: list[str]
    gaps: list[Gap]
    hops: list[RetrievalHop]
    entities_retrieved: int
    total_ms: int
    trace_summary: str = ""


@dataclass
class CoverageReport:
    """Aggregated coverage report."""
    total_questions: int
    clean_count: int
    incomplete_count: int
    missing_count: int
    clean_pct: float
    incomplete_pct: float
    missing_pct: float
    per_layer: dict[str, dict[str, int]]  # layer → {CLEAN: n, INCOMPLETE: n, MISSING: n}
    per_source: dict[str, dict[str, int]]  # seed|doc|persona|work-item → {CLEAN: n, ...}
    per_persona: dict[str, dict[str, int]]  # persona_name → {CLEAN: n, ...}
    all_gaps: list[Gap]
    results: list[EvalResult]
    total_time_s: float
    total_cost_estimate: float


# ── Question Generation ──

SEED_QUESTION_PROMPT = """You are generating eval questions for a domain knowledge base.

Below is the seed context — a high-level onboarding document for this domain. Generate {count} questions that someone new to this domain would ask.

Requirements:
- Mix of question types: process flows, system responsibilities, team ownership, terminology, cross-system interactions
- Questions should be answerable from domain knowledge, not implementation details
- Each question should target a different aspect of the domain
- Include 1-2 questions that span multiple systems or teams (cross-cutting)

Seed context:
{seed_content}

Return a JSON array of objects with fields: "question", "topic" (2-3 word label), "layer_hint" (one of: structural, behavioral, organizational, language, reference, decision, or empty if cross-cutting).

Return ONLY the JSON array, no other text."""

DOC_QUESTION_PROMPT = """You are generating eval questions from a source document that was used to build a domain knowledge base. Generate {count} questions that this document should help answer.

Requirements:
- Questions should test whether the KB captured the key knowledge from this document
- Focus on facts, relationships, processes, and decisions described in the document
- Don't ask about formatting or document structure — ask about domain knowledge
- Each question should be specific enough to have a clear answer

Document filename: {filename}
Document content:
{doc_content}

Return a JSON array of objects with fields: "question", "topic" (2-3 word label), "layer_hint" (one of: structural, behavioral, organizational, language, reference, decision, or empty if unclear).

Return ONLY the JSON array, no other text."""


async def generate_questions(
    seed_path: Path | None,
    docs_dir: Path | None,
    target_count: int = 30,
    seed_questions: int = 10,
    docs_sample_size: int = 10,
    api_key: str | None = None,
) -> list[EvalQuestion]:
    """Generate eval questions from seed context and source documents."""
    api_key = api_key or os.environ.get("LLM_API_KEY", "")
    client = None  # uses litellm via _generate_from_prompt

    questions: list[EvalQuestion] = []

    # 1. Generate from seed context
    if seed_path and seed_path.exists():
        seed_content = seed_path.read_text(encoding="utf-8")
        seed_qs = await _generate_from_prompt(
            client,
            SEED_QUESTION_PROMPT.format(count=seed_questions, seed_content=seed_content),
            source="seed",
            source_file="seed-context",
        )
        questions.extend(seed_qs)
        logger.info("seed_questions_generated", count=len(seed_qs))

    # 2. Generate from sampled source docs
    if docs_dir and docs_dir.exists():
        doc_files = sorted(docs_dir.glob("**/*.md")) + sorted(docs_dir.glob("**/*.txt"))
        if len(doc_files) > docs_sample_size:
            doc_files = random.sample(doc_files, docs_sample_size)

        remaining = target_count - len(questions)
        per_doc = max(2, remaining // max(len(doc_files), 1))

        for doc_path in doc_files:
            doc_content = doc_path.read_text(encoding="utf-8")
            # Truncate very long docs to stay within token limits
            if len(doc_content) > 8000:
                doc_content = doc_content[:8000] + "\n\n[... truncated for question generation]"

            doc_qs = await _generate_from_prompt(
                client,
                DOC_QUESTION_PROMPT.format(
                    count=per_doc,
                    filename=doc_path.name,
                    doc_content=doc_content,
                ),
                source="doc",
                source_file=doc_path.name,
            )
            questions.extend(doc_qs)
            logger.info("doc_questions_generated", file=doc_path.name, count=len(doc_qs))

    # 3. Deduplicate similar questions
    questions = _deduplicate_questions(questions)

    logger.info("total_questions_generated", count=len(questions))
    return questions


def _deduplicate_questions(questions: list[EvalQuestion]) -> list[EvalQuestion]:
    """Remove near-duplicate questions using two methods:

    1. Jaccard word similarity > 0.6 (catches rephrased questions)
    2. Topic + key entity overlap (catches semantic duplicates like
       "end-to-end claim flow" vs "how does a claim go from submission to payment")
    """
    if not questions:
        return questions

    # Common stop words to ignore in similarity
    stop_words = {
        "what", "how", "does", "the", "is", "are", "and", "or", "for", "in",
        "of", "to", "a", "an", "this", "that", "it", "be", "can", "do", "from",
        "with", "which", "when", "where", "who", "why", "should", "would", "could",
        "about", "between", "through", "during", "specific", "currently", "each",
    }

    def content_words(text: str) -> set[str]:
        """Extract meaningful words, skipping stop words."""
        words = set(re.findall(r"\w+", text.lower()))
        return words - stop_words

    deduped: list[EvalQuestion] = []
    for q in questions:
        q_words = content_words(q.question)
        is_dup = False
        for kept in deduped:
            kept_words = content_words(kept.question)
            if not q_words or not kept_words:
                continue

            # Method 1: Jaccard on content words (lower threshold now stop words removed)
            jaccard = len(q_words & kept_words) / len(q_words | kept_words)
            if jaccard > 0.55:
                is_dup = True
                logger.debug("question_dedup_jaccard", dropped=q.question[:60], similar_to=kept.question[:60], jaccard=round(jaccard, 2))
                break

            # Method 2: High overlap on longer words (likely entity/system names)
            q_entities = {w for w in q_words if len(w) >= 5}
            kept_entities = {w for w in kept_words if len(w) >= 5}
            if q_entities and kept_entities:
                entity_overlap = len(q_entities & kept_entities) / min(len(q_entities), len(kept_entities))
                if entity_overlap > 0.7:
                    is_dup = True
                    logger.debug("question_dedup_entity", dropped=q.question[:60], similar_to=kept.question[:60], overlap=round(entity_overlap, 2))
                    break

        if not is_dup:
            deduped.append(q)

    if len(deduped) < len(questions):
        logger.info("questions_deduped", before=len(questions), after=len(deduped))

    return deduped


# ── Persona Completeness Checks ──

PERSONA_QUESTION_PROMPT = """You are evaluating a domain knowledge base for completeness from a specific persona's perspective.

Persona: {persona_label}
Description: {persona_description}

Below is the seed context — a high-level overview of this domain. Based on the persona's needs, generate {count} specific questions that test whether the knowledge base has adequate coverage.

The checks below are hints about what this persona needs. Generate concrete, domain-specific questions based on the actual systems, teams, and processes mentioned in the seed context.

Checks:
{checks}

Seed context:
{seed_content}

Requirements:
- Each question should be specific to THIS domain (reference actual systems, teams, processes from the seed)
- Questions should be answerable from a well-maintained KB — not trick questions
- Mix of simple factual questions and deeper "how does X work?" questions
- IMPORTANT: Do NOT repeat topics already covered by these existing questions:
{existing_questions}

Return a JSON array of objects with fields: "question", "topic" (2-3 word label), "layer_hint" (one of: structural, behavioral, organizational, language, reference, decision, or empty if cross-cutting).

Return ONLY the JSON array, no other text."""


def load_persona_templates(config_path: Path | None = None) -> dict:
    """Load persona templates from YAML config.

    Falls back to the default config shipped with the package.
    """
    import yaml

    if config_path and config_path.exists():
        return yaml.safe_load(config_path.read_text(encoding="utf-8"))

    # Default: shipped config
    default_path = Path(__file__).parent.parent / "config" / "persona-templates.yaml"
    if default_path.exists():
        return yaml.safe_load(default_path.read_text(encoding="utf-8"))

    logger.warning("persona_templates_not_found")
    return {"personas": {}}


async def generate_persona_questions(
    seed_path: Path,
    config_path: Path | None = None,
    personas: list[str] | None = None,
    questions_per_persona: int = 5,
    existing_questions: list[EvalQuestion] | None = None,
    api_key: str | None = None,
) -> list[EvalQuestion]:
    """Generate completeness check questions from persona templates.

    Args:
        seed_path: Path to seed context file.
        config_path: Optional path to custom persona-templates.yaml.
        personas: Optional list of persona keys to use (default: all).
        questions_per_persona: Number of questions per persona.
        existing_questions: Already-generated questions to avoid overlap with.
        api_key: LLM API key.
    """
    api_key = api_key or os.environ.get("LLM_API_KEY", "")
    client = None  # uses litellm via _generate_from_prompt

    config = load_persona_templates(config_path)
    all_personas = config.get("personas", {})

    if personas:
        all_personas = {k: v for k, v in all_personas.items() if k in personas}

    if not all_personas:
        logger.warning("no_personas_configured")
        return []

    seed_content = seed_path.read_text(encoding="utf-8")
    questions: list[EvalQuestion] = []

    # Build existing questions text for overlap avoidance
    all_existing = list(existing_questions or []) + questions
    existing_text = "(none yet)"

    for persona_key, persona_config in all_personas.items():
        checks_text = "\n".join(f"- {c}" for c in persona_config.get("checks", []))

        # Update existing questions text to include previous personas too
        if all_existing:
            existing_text = "\n".join(f"- {q.question}" for q in all_existing)

        prompt = PERSONA_QUESTION_PROMPT.format(
            persona_label=persona_config.get("label", persona_key),
            persona_description=persona_config.get("description", ""),
            count=questions_per_persona,
            checks=checks_text,
            seed_content=seed_content,
            existing_questions=existing_text,
        )

        persona_qs = await _generate_from_prompt(
            client, prompt,
            source="persona",
            source_file=persona_key,
        )

        # Tag each question with the persona
        for q in persona_qs:
            q.persona = persona_key

        questions.extend(persona_qs)
        all_existing.extend(persona_qs)
        logger.info("persona_questions_generated", persona=persona_key, count=len(persona_qs))

    return questions


# ── Work Item Parser (DDC) ──

def load_work_items(work_items_dir: Path) -> list[EvalQuestion]:
    """Parse work items (tickets, incidents) from a directory as eval questions.

    Supports markdown and text files. Each file = one work item.
    Uses full ticket content as the question — the retrieval pipeline needs
    the diagnostic context (severity, symptoms, what they're trying to do)
    to find the right entities.
    """
    if not work_items_dir.exists():
        logger.warning("work_items_dir_not_found", path=str(work_items_dir))
        return []

    questions: list[EvalQuestion] = []
    files = sorted(work_items_dir.glob("**/*.md")) + sorted(work_items_dir.glob("**/*.txt"))

    for filepath in files:
        content = filepath.read_text(encoding="utf-8").strip()
        if not content:
            continue

        # Extract title from first heading or first line
        lines = content.split("\n")
        title = lines[0].lstrip("#").strip()

        # Use full content as the question — truncate only if very long
        question_text = content
        if len(question_text) > 2000:
            question_text = question_text[:2000] + "\n\n[... truncated]"

        questions.append(EvalQuestion(
            question=question_text,
            source="work-item",
            source_file=filepath.stem,
            topic=title[:50],
        ))

    logger.info("work_items_loaded", count=len(questions), dir=str(work_items_dir))
    return questions


async def _generate_from_prompt(
    client,
    prompt: str,
    source: str,
    source_file: str,
) -> list[EvalQuestion]:
    """Call LLM to generate questions from a prompt.

    Uses litellm for provider-agnostic LLM calls. The client parameter
    is ignored (kept for backwards compatibility).
    """
    import litellm
    from context_blocks.config import get_settings

    settings = get_settings()
    provider = os.environ.get("LLM_PROVIDER", "anthropic")
    model = os.environ.get("LLM_MODEL", "claude-sonnet-4-6")
    api_key = os.environ.get("LLM_API_KEY", "")
    litellm.request_timeout = int(settings.llm_request_timeout)
    litellm_model = model if provider == "openai" else f"{provider}/{model}"

    try:
        response = litellm.completion(
            model=litellm_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            api_key=api_key,
        )
    except Exception as e:
        logger.error("question_generation_api_error", source=source_file, error=str(e))
        return []

    text = response.choices[0].message.content.strip()

    # Parse JSON — handle markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    try:
        items = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("question_generation_parse_failed", source=source_file, text=text[:200])
        return []

    questions = []
    for item in items:
        if isinstance(item, dict) and "question" in item:
            questions.append(EvalQuestion(
                question=item["question"],
                source=source,
                source_file=source_file,
                layer_hint=item.get("layer_hint", ""),
                topic=item.get("topic", ""),
            ))

    logger.info(
        "questions_parsed",
        source=source_file,
        count=len(questions),
        input_tokens=getattr(response.usage, "prompt_tokens", 0),
        output_tokens=getattr(response.usage, "completion_tokens", 0),
    )

    return questions


# ── Eval Runner ──

async def run_eval(
    questions: list[EvalQuestion],
    pipeline,  # RetrievalPipeline
) -> list[EvalResult]:
    """Run each question through the retrieval pipeline and collect results."""
    results: list[EvalResult] = []

    for i, q in enumerate(questions):
        logger.info("eval_question", index=i + 1, total=len(questions), question=q.question[:80])

        t0 = time.time()
        try:
            retrieval_result: RetrievalResult = await pipeline.retrieve(q.question)
        except Exception as e:
            logger.error("eval_question_failed", index=i + 1, question=q.question[:80], error=str(e))
            # Record as MISSING with error info — don't kill the whole run
            results.append(EvalResult(
                question=q,
                answer=f"[ERROR] Retrieval failed: {e}",
                score=AnswerScore.NOT_ANSWERABLE,
                ddc_class="MISSING",
                citations=[],
                gaps=[],
                hops=[],
                entities_retrieved=0,
                total_ms=int((time.time() - t0) * 1000),
                trace_summary="(retrieval error)",
            ))
            continue
        elapsed_ms = int((time.time() - t0) * 1000)

        # Build trace summary
        trace_parts = []
        for hop in retrieval_result.trace.hops[:5]:
            trace_parts.append(
                f"{hop.entity_name} ({hop.entity_type}, {hop.matched_by}, "
                f"conf={hop.confidence:.0%})"
            )
        trace_summary = " → ".join(trace_parts) if trace_parts else "(no hops)"

        results.append(EvalResult(
            question=q,
            answer=retrieval_result.answer,
            score=retrieval_result.score,
            ddc_class=DDC_TAXONOMY[retrieval_result.score],
            citations=retrieval_result.citations,
            gaps=retrieval_result.gaps,
            hops=retrieval_result.trace.hops,
            entities_retrieved=retrieval_result.trace.total_entities_retrieved,
            total_ms=elapsed_ms,
            trace_summary=trace_summary,
        ))

    return results


# ── Coverage Report ──

def build_coverage_report(
    results: list[EvalResult],
    total_time_s: float,
) -> CoverageReport:
    """Aggregate eval results into a coverage report."""
    total = len(results)
    if total == 0:
        return CoverageReport(
            total_questions=0, clean_count=0, incomplete_count=0, missing_count=0,
            clean_pct=0, incomplete_pct=0, missing_pct=0,
            per_layer={}, per_source={}, per_persona={}, all_gaps=[], results=[],
            total_time_s=0, total_cost_estimate=0,
        )

    clean = sum(1 for r in results if r.ddc_class == "CLEAN")
    incomplete = sum(1 for r in results if r.ddc_class == "INCOMPLETE")
    missing = sum(1 for r in results if r.ddc_class == "MISSING")

    # Per-layer breakdown (using layer_hint from questions)
    per_layer: dict[str, dict[str, int]] = {}
    for r in results:
        layer = r.question.layer_hint or "unclassified"
        if layer not in per_layer:
            per_layer[layer] = {"CLEAN": 0, "INCOMPLETE": 0, "MISSING": 0}
        per_layer[layer][r.ddc_class] += 1

    # Per-source breakdown
    per_source: dict[str, dict[str, int]] = {}
    for r in results:
        src = r.question.source
        if src not in per_source:
            per_source[src] = {"CLEAN": 0, "INCOMPLETE": 0, "MISSING": 0}
        per_source[src][r.ddc_class] += 1

    # Per-persona breakdown
    per_persona: dict[str, dict[str, int]] = {}
    for r in results:
        if r.question.persona:
            p = r.question.persona
            if p not in per_persona:
                per_persona[p] = {"CLEAN": 0, "INCOMPLETE": 0, "MISSING": 0}
            per_persona[p][r.ddc_class] += 1

    # Collect all gaps
    all_gaps = []
    for r in results:
        all_gaps.extend(r.gaps)

    # Cost estimate: ~$0.02 per question (synthesis dominates)
    cost_estimate = total * 0.02

    return CoverageReport(
        total_questions=total,
        clean_count=clean,
        incomplete_count=incomplete,
        missing_count=missing,
        clean_pct=round(clean / total * 100, 1),
        incomplete_pct=round(incomplete / total * 100, 1),
        missing_pct=round(missing / total * 100, 1),
        per_layer=per_layer,
        per_source=per_source,
        per_persona=per_persona,
        all_gaps=all_gaps,
        results=results,
        total_time_s=round(total_time_s, 1),
        total_cost_estimate=round(cost_estimate, 2),
    )


# ── Report Writer ──

def write_eval_report(report: CoverageReport, output_path: Path) -> None:
    """Write coverage report as markdown."""
    lines = [
        "# KB Coverage Report",
        "",
        f"**Generated:** {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Questions:** {report.total_questions}",
        f"**Time:** {report.total_time_s}s",
        f"**Estimated cost:** ${report.total_cost_estimate:.2f}",
        "",
        "## Coverage Summary",
        "",
        "| DDC Class | Count | % |",
        "|-----------|-------|---|",
        f"| CLEAN (answerable) | {report.clean_count} | {report.clean_pct}% |",
        f"| INCOMPLETE (partial) | {report.incomplete_count} | {report.incomplete_pct}% |",
        f"| MISSING (not answerable) | {report.missing_count} | {report.missing_pct}% |",
        "",
    ]

    # Per-source breakdown
    if report.per_source:
        lines.extend([
            "## By Question Source",
            "",
            "| Source | CLEAN | INCOMPLETE | MISSING | Total |",
            "|--------|-------|------------|---------|-------|",
        ])
        for src, counts in sorted(report.per_source.items()):
            total = sum(counts.values())
            lines.append(
                f"| {src} | {counts['CLEAN']} | {counts['INCOMPLETE']} | {counts['MISSING']} | {total} |"
            )
        lines.append("")

    # Per-layer breakdown
    if report.per_layer:
        lines.extend([
            "## By Knowledge Layer",
            "",
            "| Layer | CLEAN | INCOMPLETE | MISSING | Total | Coverage |",
            "|-------|-------|------------|---------|-------|----------|",
        ])
        for layer, counts in sorted(report.per_layer.items()):
            total = sum(counts.values())
            coverage = round(counts["CLEAN"] / total * 100) if total > 0 else 0
            lines.append(
                f"| {layer} | {counts['CLEAN']} | {counts['INCOMPLETE']} | {counts['MISSING']} | {total} | {coverage}% |"
            )
        lines.append("")

    # Per-persona breakdown
    if report.per_persona:
        lines.extend([
            "## By Persona",
            "",
            "| Persona | CLEAN | INCOMPLETE | MISSING | Total | Coverage |",
            "|---------|-------|------------|---------|-------|----------|",
        ])
        for persona, counts in sorted(report.per_persona.items()):
            total = sum(counts.values())
            coverage = round(counts["CLEAN"] / total * 100) if total > 0 else 0
            lines.append(
                f"| {persona} | {counts['CLEAN']} | {counts['INCOMPLETE']} | {counts['MISSING']} | {total} | {coverage}% |"
            )
        lines.append("")

    # Individual results
    lines.extend([
        "## Question Results",
        "",
        "| # | Source | Question | Score | Entities | Time |",
        "|---|--------|----------|-------|----------|------|",
    ])
    for i, r in enumerate(report.results):
        q_short = r.question.question[:60] + ("..." if len(r.question.question) > 60 else "")
        lines.append(
            f"| {i+1} | {r.question.source} | {q_short} | **{r.ddc_class}** | {r.entities_retrieved} | {r.total_ms}ms |"
        )
    lines.append("")

    # Detailed results with answers and traces
    lines.extend([
        "## Detailed Results",
        "",
    ])
    for i, r in enumerate(report.results):
        icon = {"CLEAN": "✅", "INCOMPLETE": "⚠️", "MISSING": "❌"}.get(r.ddc_class, "")
        lines.extend([
            f"### Q{i+1}: {r.question.question}",
            f"**Source:** {r.question.source} ({r.question.source_file}) | "
            f"**Score:** {icon} {r.ddc_class} | "
            f"**Entities:** {r.entities_retrieved} | **Time:** {r.total_ms}ms",
            "",
            f"**Answer:** {r.answer[:500]}{'...' if len(r.answer) > 500 else ''}",
            "",
        ])

        # Full hop-by-hop trace
        if r.hops:
            lines.append("**Retrieval Trace:**")
            lines.append("| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |")
            lines.append("|-----|--------|------|-------|----------|------------|-------|-----|")
            for hop in r.hops:
                via = ""
                if hop.relationship_from:
                    via = f"{hop.relationship_type} from {hop.relationship_from}"
                gap_marker = " ⚠️" if hop.gap_flag else ""
                found = "+".join(hop.found_by) if hop.found_by else hop.matched_by
                lines.append(
                    f"| {hop.hop_number} | {hop.entity_name}{gap_marker} | "
                    f"{hop.entity_type} | {hop.layer} | {found} | "
                    f"{hop.confidence:.0%} | {hop.fused_score:.3f} | {via} |"
                )
            lines.append("")
        else:
            lines.append("**Trace:** (no hops)")
            lines.append("")
        if r.gaps:
            lines.append("**Gaps:**")
            for gap in r.gaps:
                lines.append(f"- [{gap.severity}] {gap.gap_type}: {gap.description}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Gap summary
    if report.all_gaps:
        # Deduplicate gaps by description
        seen = set()
        unique_gaps = []
        for gap in report.all_gaps:
            if gap.description not in seen:
                seen.add(gap.description)
                unique_gaps.append(gap)

        gap_by_type: dict[str, list[Gap]] = {}
        for gap in unique_gaps:
            gap_by_type.setdefault(gap.gap_type, []).append(gap)

        lines.extend([
            "## Gap Summary",
            "",
            f"**Total unique gaps:** {len(unique_gaps)}",
            "",
        ])
        for gap_type, gaps in sorted(gap_by_type.items()):
            lines.append(f"### {gap_type} ({len(gaps)})")
            for gap in gaps[:10]:  # Cap at 10 per type
                lines.append(f"- [{gap.severity}] {gap.description}")
                lines.append(f"  → {gap.suggested_action}")
            if len(gaps) > 10:
                lines.append(f"- ... and {len(gaps) - 10} more")
            lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("eval_report_written", path=str(output_path), questions=report.total_questions)


def write_eval_json(results: list[EvalResult], output_path: Path) -> None:
    """Write raw eval results as JSON for programmatic access."""
    data = []
    for r in results:
        data.append({
            "question": r.question.question,
            "source": r.question.source,
            "source_file": r.question.source_file,
            "layer_hint": r.question.layer_hint,
            "topic": r.question.topic,
            "persona": r.question.persona,
            "score": r.score.value,
            "ddc_class": r.ddc_class,
            "answer": r.answer,
            "citations": r.citations,
            "entities_retrieved": r.entities_retrieved,
            "total_ms": r.total_ms,
            "trace_summary": r.trace_summary,
            "hops": [
                {
                    "hop_number": h.hop_number,
                    "entity_id": h.entity_id,
                    "entity_name": h.entity_name,
                    "entity_type": h.entity_type,
                    "layer": h.layer,
                    "matched_by": h.matched_by,
                    "confidence": h.confidence,
                    "fused_score": h.fused_score,
                    "relationship_from": h.relationship_from,
                    "relationship_type": h.relationship_type,
                    "gap_flag": h.gap_flag,
                    "gap_reason": h.gap_reason,
                    "found_by": h.found_by,
                }
                for h in r.hops
            ],
            "gaps": [
                {
                    "gap_type": g.gap_type,
                    "entity_id": g.entity_id,
                    "description": g.description,
                    "severity": g.severity,
                }
                for g in r.gaps
            ],
        })

    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    logger.info("eval_json_written", path=str(output_path), results=len(data))
