"""Baseline retrieval pipelines for DCR paper comparison.

Three conditions:
  1. NaiveVectorPipeline — cosine similarity only, top-K, no fusion, no graph
  2. VanillaRAGPipeline — vector + keyword, simple merge, no typed traversal
  3. RetrievalPipeline (existing) — full DCR with all 7 stages

All share the same backend, embedder, and synthesizer so the only variable
is the retrieval strategy.
"""
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import structlog

from context_blocks.retrieval.backend import StorageBackend
from context_blocks.retrieval.types import (
    AnswerScore,
    Gap,
    RetrievalHop,
    RetrievalResult,
    RetrievalTrace,
    ScoredEntity,
    StageTrace,
)

logger = structlog.get_logger(__name__)


def _write_baseline_trace(
    pipeline_name: str,
    question: str,
    hops: list,
    context_text: str,
    answer: str,
    score,
    citations: list[str],
    stage_info: dict,
    total_ms: int,
    synthesis_ms: int,
) -> None:
    """Write a trace file for a baseline pipeline run."""
    traces_dir = Path(".private/traces")
    traces_dir.mkdir(parents=True, exist_ok=True)

    slug = re.sub(r'[^a-z0-9]+', '-', question.lower())[:60].strip('-')
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-{pipeline_name}-{slug}.md"

    ddc_map = {"answerable": "CLEAN", "partial": "INCOMPLETE", "not_answerable": "MISSING"}
    ddc_class = ddc_map.get(score.value, score.value) if score else "?"

    lines = [
        f"# Trace: {pipeline_name}",
        f"**Question:** {question}",
        f"**Score:** {ddc_class} | **Time:** {total_ms}ms (synthesis: {synthesis_ms}ms)",
        f"**Entities retrieved:** {len(hops)}",
        "",
        "## Search Results",
        "",
    ]

    for key, val in stage_info.items():
        lines.append(f"- **{key}:** {val}")
    lines.append("")

    lines.extend([
        "## Retrieved Entities",
        "",
        "| # | Entity | Type | Layer | Found By | Score | Confidence |",
        "|---|--------|------|-------|----------|-------|------------|",
    ])
    for i, hop in enumerate(hops):
        found = "+".join(hop.found_by) if hop.found_by else hop.matched_by
        lines.append(
            f"| {i+1} | {hop.entity_name} | {hop.entity_type} | "
            f"{hop.layer} | {found} | {hop.fused_score:.3f} | {hop.confidence:.0%} |"
        )
    lines.append("")

    lines.extend([
        "## Context Sent to LLM",
        "",
        f"({len(context_text)} chars, ~{len(context_text)//4} tokens)",
        "",
        "```",
        context_text,
        "```",
        "",
        "## Answer",
        "",
        f"**Score:** {ddc_class}",
        f"**Citations:** {', '.join(citations) if citations else '(none)'}",
        "",
        answer,
    ])

    (traces_dir / filename).write_text("\n".join(lines))
    logger.info("baseline_trace_written", file=filename, pipeline=pipeline_name)


class NaiveVectorPipeline:
    """Baseline 1: Pure vector search + synthesis.

    No intent classification, no keyword search, no graph traversal,
    no fusion, no confidence weighting, no dedup, no gap detection.
    Just cosine similarity → top K → synthesize.
    """

    def __init__(self, backend: StorageBackend, embed_fn=None, synthesize_fn=None, config=None):
        self.backend = backend
        self.embed_fn = embed_fn
        self.synthesize_fn = synthesize_fn
        self.max_results = (config or {}).get("max_results", 15)
        self.token_budget = (config or {}).get("token_budget", 24000)

    def _resolve_rel_name(self, target_id: str) -> str:
        entity = self.backend.entities.get(target_id)
        return entity.name if entity else target_id

    async def retrieve(self, question: str, full_trace: bool = False, **kwargs) -> RetrievalResult:
        start_time = time.time()

        # Just vector search
        if not self.embed_fn:
            return self._empty_result(question, start_time)

        query_embedding = await self.embed_fn(question)
        vector_results = await self.backend.vector_search(query_embedding, top_k=self.max_results)

        # Build context directly from top results — no scoring adjustments
        context_parts = []
        hops = []
        tokens_used = 0

        entities = vector_results[:self.max_results]
        total_score = sum(e.score for e in entities) or 1.0
        TOKEN_FLOOR = 250
        TOKEN_CEILING = 2500

        for entity in entities:
            raw_share = int(self.token_budget * (entity.score / total_score))
            body_token_budget = max(TOKEN_FLOOR, min(TOKEN_CEILING, raw_share))

            block = f"Entity: {entity.name} ({entity.entity_type})\nDescription: {entity.description}\n"

            body_text = entity.body.strip() if entity.body else ""
            if body_text:
                body_text = re.split(r'\n##\s*Open Questions', body_text)[0].strip()
            if body_text:
                body_char_budget = body_token_budget * 4
                if len(body_text) > body_char_budget:
                    body_text = body_text[:body_char_budget].rsplit("\n", 1)[0] + "\n[...]"
                block += f"\n{body_text}\n"

            block_tokens = len(block) // 4
            if tokens_used + block_tokens > self.token_budget:
                break
            context_parts.append(block)
            tokens_used += block_tokens

            hops.append(RetrievalHop(
                entity_id=entity.entity_id,
                entity_name=entity.name,
                entity_type=entity.entity_type,
                layer=entity.layer,
                confidence=entity.confidence,
                hop_number=0,
                matched_by="vector",
                fused_score=entity.score,
                found_by=["vector"],
            ))

        context_text = "\n---\n".join(context_parts)

        # Synthesize
        t6 = time.time()
        if self.synthesize_fn:
            answer, score, citations = await self.synthesize_fn(question, context_text, {})
        else:
            answer = "(No synthesis)"
            score = AnswerScore.PARTIAL
            citations = []
        synthesis_ms = int((time.time() - t6) * 1000)

        total_ms = int((time.time() - start_time) * 1000)

        if full_trace:
            _write_baseline_trace(
                "naive_vector", question, hops, context_text,
                answer, score, citations,
                {"vector_candidates": len(vector_results), "selected": len(hops)},
                total_ms, synthesis_ms,
            )

        trace = RetrievalTrace(
            question=question,
            sub_queries=[question],
            intent_weights={},
            hops=hops,
            stage_trace=StageTrace(
                vector_candidates=len(vector_results),
                keyword_candidates=0,
                graph_candidates=0,
                fused_unique=len(vector_results),
                after_dedup=len(hops),
                context_selected=len(hops),
            ),
            total_entities_searched=self.backend.entity_count(),
            total_entities_retrieved=len(hops),
            synthesis_ms=synthesis_ms,
            total_ms=total_ms,
        )

        return RetrievalResult(
            answer=answer,
            citations=citations,
            score=score,
            trace=trace,
            gaps=[],
            context_text=context_text,
        )

    def _empty_result(self, question, start_time):
        return RetrievalResult(
            answer="No embedder available.",
            citations=[], score=AnswerScore.NOT_ANSWERABLE,
            trace=RetrievalTrace(question=question, sub_queries=[], intent_weights={},
                                 total_ms=int((time.time() - start_time) * 1000)),
            gaps=[], context_text="",
        )


class VanillaRAGPipeline:
    """Baseline 2: Vector + keyword search with simple merge.

    Has: vector search, keyword search, basic score merge.
    Missing: intent classification, typed graph traversal, layer priority boost,
    confidence weighting, 5-layer dedup, gap detection.
    """

    def __init__(self, backend: StorageBackend, embed_fn=None, synthesize_fn=None, config=None):
        self.backend = backend
        self.embed_fn = embed_fn
        self.synthesize_fn = synthesize_fn
        self.max_results = (config or {}).get("max_results", 15)
        self.token_budget = (config or {}).get("token_budget", 24000)

    def _resolve_rel_name(self, target_id: str) -> str:
        entity = self.backend.entities.get(target_id)
        return entity.name if entity else target_id

    async def retrieve(self, question: str, full_trace: bool = False, **kwargs) -> RetrievalResult:
        start_time = time.time()

        # Vector search
        query_embedding = None
        vector_results = []
        if self.embed_fn:
            query_embedding = await self.embed_fn(question)
            entity_count = self.backend.entity_count()
            top_k = max(20, min(200, entity_count // 5))
            vector_results = await self.backend.vector_search(query_embedding, top_k=top_k)

        # Keyword search
        entity_count = self.backend.entity_count()
        top_k = max(20, min(200, entity_count // 5))
        keyword_results = await self.backend.keyword_search(question, top_k=top_k)

        # Simple merge — combine scores, no RRF, no layer boost
        entity_scores: dict[str, float] = {}
        entity_map: dict[str, ScoredEntity] = {}

        for entity in vector_results:
            entity_scores[entity.entity_id] = entity.score
            entity_map[entity.entity_id] = entity

        for entity in keyword_results:
            if entity.entity_id in entity_scores:
                entity_scores[entity.entity_id] = (entity_scores[entity.entity_id] + entity.score) / 2
            else:
                entity_scores[entity.entity_id] = entity.score
                entity_map[entity.entity_id] = entity

        # Sort by score, take top K
        sorted_ids = sorted(entity_scores, key=lambda x: -entity_scores[x])[:self.max_results]

        # Build context
        context_parts = []
        hops = []
        tokens_used = 0

        total_score = sum(entity_scores[eid] for eid in sorted_ids) or 1.0
        TOKEN_FLOOR = 250
        TOKEN_CEILING = 2500

        for eid in sorted_ids:
            entity = entity_map[eid]
            raw_share = int(self.token_budget * (entity_scores[eid] / total_score))
            body_token_budget = max(TOKEN_FLOOR, min(TOKEN_CEILING, raw_share))

            block = f"Entity: {entity.name} ({entity.entity_type})\nDescription: {entity.description}\n"

            rels = [
                f"  {r['type']} → {self._resolve_rel_name(r['target_id'])}"
                for r in entity.relationships[:5]
            ]
            if rels:
                block += "Relationships:\n" + "\n".join(rels) + "\n"

            body_text = entity.body.strip() if entity.body else ""
            if body_text:
                body_text = re.split(r'\n##\s*Open Questions', body_text)[0].strip()
            if body_text:
                body_char_budget = body_token_budget * 4
                if len(body_text) > body_char_budget:
                    body_text = body_text[:body_char_budget].rsplit("\n", 1)[0] + "\n[...]"
                block += f"\n{body_text}\n"

            block_tokens = len(block) // 4
            if tokens_used + block_tokens > self.token_budget:
                break
            context_parts.append(block)
            tokens_used += block_tokens

            found_by = []
            if any(e.entity_id == eid for e in vector_results):
                found_by.append("vector")
            if any(e.entity_id == eid for e in keyword_results):
                found_by.append("keyword")

            hops.append(RetrievalHop(
                entity_id=entity.entity_id,
                entity_name=entity.name,
                entity_type=entity.entity_type,
                layer=entity.layer,
                confidence=entity.confidence,
                hop_number=0,
                matched_by=found_by[0] if found_by else "unknown",
                fused_score=entity_scores[eid],
                found_by=found_by,
            ))

        context_text = "\n---\n".join(context_parts)

        # Synthesize
        t6 = time.time()
        if self.synthesize_fn:
            answer, score, citations = await self.synthesize_fn(question, context_text, {})
        else:
            answer = "(No synthesis)"
            score = AnswerScore.PARTIAL
            citations = []
        synthesis_ms = int((time.time() - t6) * 1000)

        total_ms = int((time.time() - start_time) * 1000)

        if full_trace:
            _write_baseline_trace(
                "vanilla_rag", question, hops, context_text,
                answer, score, citations,
                {
                    "vector_candidates": len(vector_results),
                    "keyword_candidates": len(keyword_results),
                    "fused_unique": len(entity_scores),
                    "selected": len(hops),
                },
                total_ms, synthesis_ms,
            )

        trace = RetrievalTrace(
            question=question,
            sub_queries=[question],
            intent_weights={},
            hops=hops,
            stage_trace=StageTrace(
                vector_candidates=len(vector_results),
                keyword_candidates=len(keyword_results),
                graph_candidates=0,
                fused_unique=len(entity_scores),
                after_dedup=len(hops),
                context_selected=len(hops),
            ),
            total_entities_searched=self.backend.entity_count(),
            total_entities_retrieved=len(hops),
            synthesis_ms=synthesis_ms,
            total_ms=total_ms,
        )

        return RetrievalResult(
            answer=answer,
            citations=citations,
            score=score,
            trace=trace,
            gaps=[],
            context_text=context_text,
        )
