"""Tests for the retrieval pipeline — query understanding, fusion, scoring, dedup, gap detection."""

import asyncio
import math
from collections import defaultdict

import numpy as np
import pytest

from context_blocks.retrieval.query_understanding import classify_query
from context_blocks.retrieval.types import (
    AnswerScore,
    Gap,
    QueryUnderstanding,
    RetrievalHop,
    ScoredEntity,
)


# ── Fixtures ──

def _make_entity(
    entity_id: str,
    name: str,
    entity_type: str = "system",
    layer: str = "structural",
    confidence: float = 0.9,
    score: float = 0.5,
    matched_by: str = "keyword",
    relationships: list | None = None,
    source_documents: list | None = None,
    description: str = "",
    hop_number: int = 0,
) -> ScoredEntity:
    return ScoredEntity(
        entity_id=entity_id,
        name=name,
        entity_type=entity_type,
        layer=layer,
        confidence=confidence,
        description=description or f"Description of {name}",
        overview="",
        body=f"Body text for {name}",
        relationships=relationships or [],
        source_documents=source_documents or [],
        score=score,
        matched_by=matched_by,
        hop_number=hop_number,
    )


# ── Query Understanding Tests ──

class TestQueryUnderstanding:
    def test_process_query_detected(self):
        result = classify_query("How does a claim flow from submission to payment?")
        assert "process" in result.intent_weights
        assert result.intent_weights["process"] > 0

    def test_entity_query_detected(self):
        result = classify_query("What is the Rules Engine?")
        assert "entity" in result.intent_weights
        assert result.intent_weights["entity"] > 0

    def test_ownership_query_detected(self):
        result = classify_query("Who owns the Payment Engine?")
        assert "ownership" in result.intent_weights
        assert result.intent_weights["ownership"] > 0

    def test_listing_query_flag(self):
        result = classify_query("List all systems in the platform")
        assert result.is_listing_query is True

    def test_comparison_query_flag(self):
        result = classify_query("Compare the old and new fraud detection systems")
        assert result.is_comparison_query is True

    def test_multi_intent(self):
        # "workflow" triggers process, "who manages" triggers ownership
        result = classify_query("Who manages the workflow for handling fraud claims?")
        assert len(result.intent_weights) >= 2

    def test_original_question_preserved(self):
        q = "What is the Claims Gateway?"
        result = classify_query(q)
        assert result.original_question == q

    def test_keywords_extracted(self):
        result = classify_query("How does the Payment Engine handle refunds?")
        assert len(result.keywords) > 0

    def test_layer_priorities_non_negative(self):
        result = classify_query("Who is responsible for the claims process?")
        for layer, priority in result.layer_priorities.items():
            assert priority >= 1.0, f"Layer {layer} has priority {priority} < 1.0"

    def test_diagnostic_query(self):
        result = classify_query("What's missing from the claims documentation?")
        assert "diagnostic" in result.intent_weights


# ── RRF Fusion Tests ──

class TestRRFFusion:
    """Test RRF scoring logic directly."""

    def test_rrf_basic_ranking(self):
        """Entity appearing in multiple lists should score higher."""
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        backend.entity_count.return_value = 10
        pipeline = RetrievalPipeline(backend)

        # Entity A appears in both vector and keyword, B only in vector
        entity_a = _make_entity("a", "Entity A", score=0.8, matched_by="vector")
        entity_b = _make_entity("b", "Entity B", score=0.9, matched_by="vector")
        entity_a_kw = _make_entity("a", "Entity A", score=0.5, matched_by="keyword")

        understanding = QueryUnderstanding(
            original_question="test",
            intent_weights={},
            layer_priorities={},
        )

        fused = pipeline._stage2_fusion(
            vector_results=[entity_a, entity_b],
            keyword_results=[entity_a_kw],
            graph_results=[],
            understanding=understanding,
            query_embedding=None,
        )

        # A should rank higher than B (appears in both lists)
        a_score = next(e.score for e in fused if e.entity_id == "a")
        b_score = next(e.score for e in fused if e.entity_id == "b")
        assert a_score > b_score

    def test_rrf_empty_lists(self):
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        understanding = QueryUnderstanding(
            original_question="test",
            intent_weights={},
            layer_priorities={},
        )

        fused = pipeline._stage2_fusion([], [], [], understanding, None)
        assert fused == []


# ── Scoring Tests ──

class TestScoring:
    def test_confidence_boost_linear(self):
        """Confidence boost should be linear: 0.5 + 0.5 * confidence."""
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend, config={"bottom_cutoff": 0})

        high_conf = _make_entity("a", "High", confidence=1.0, score=1.0)
        low_conf = _make_entity("b", "Low", confidence=0.5, score=1.0)

        results = [high_conf, low_conf]
        pipeline._stage3_scoring(results)

        # conf=1.0 → factor=1.0, conf=0.5 → factor=0.75
        assert high_conf.score > low_conf.score

    def test_bottom_cutoff_skips_low_scores(self):
        """Entities in the bottom cutoff range should not get boosted."""
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend, config={"bottom_cutoff": 0.5})

        high = _make_entity("a", "High", score=1.0, confidence=0.9)
        low = _make_entity("b", "Low", score=0.1, confidence=0.9)

        original_low_score = low.score
        pipeline._stage3_scoring([high, low])

        # Low score entity should not be boosted (in bottom 50%)
        assert low.score == original_low_score

    def test_relationship_density_boost(self):
        """Entities with more relationships should score slightly higher."""
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend, config={"bottom_cutoff": 0})

        connected = _make_entity("a", "Connected", score=1.0,
                                 relationships=[{"type": "r", "target_id": f"t{i}"} for i in range(5)])
        isolated = _make_entity("b", "Isolated", score=1.0, relationships=[])

        pipeline._stage3_scoring([connected, isolated])
        assert connected.score > isolated.score


# ── Dedup Tests ──

class TestDedup:
    def test_exact_id_dedup(self):
        """Duplicate entity IDs should be deduplicated, keeping highest score."""
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        e1 = _make_entity("a", "Entity A", score=0.8)
        e2 = _make_entity("a", "Entity A", score=0.5)

        understanding = QueryUnderstanding(
            original_question="test", intent_weights={}, layer_priorities={},
        )

        deduped = pipeline._stage4_dedup([e1, e2], understanding)
        assert len(deduped) == 1
        assert deduped[0].score == 0.8

    def test_text_similarity_dedup(self):
        """Entities with very similar descriptions should be deduplicated."""
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend, config={"text_similarity_threshold": 0.85})

        e1 = _make_entity("a", "Entity A", score=0.8,
                          description="The claims processing system handles all incoming claims")
        e2 = _make_entity("b", "Entity B", score=0.5,
                          description="The claims processing system handles all incoming claims submissions")

        understanding = QueryUnderstanding(
            original_question="test", intent_weights={}, layer_priorities={},
            is_listing_query=True,  # Skip type/layer diversity
        )

        deduped = pipeline._stage4_dedup([e1, e2], understanding)
        assert len(deduped) == 1

    def test_listing_query_skips_type_diversity(self):
        """Listing queries should not enforce type diversity limits."""
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        # 5 systems — type diversity would normally cap these
        entities = [_make_entity(f"s{i}", f"System {i}", entity_type="system",
                                 score=1.0 - i * 0.1,
                                 description=f"Unique description for system {i} with special words {i}")
                    for i in range(5)]

        listing_q = QueryUnderstanding(
            original_question="List all systems",
            intent_weights={}, layer_priorities={},
            is_listing_query=True,
        )

        deduped = pipeline._stage4_dedup(entities, listing_q)
        assert len(deduped) == 5


# ── Gap Detection Tests ──

class TestGapDetection:
    def test_low_confidence_hub_detected(self):
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        hops = [RetrievalHop(
            entity_id="e1", entity_name="Weak Entity", entity_type="system",
            layer="structural", confidence=0.3, hop_number=0,
            matched_by="keyword", fused_score=0.5,
        )]

        gaps = pipeline._stage7_gaps(hops, AnswerScore.PARTIAL, "test question")
        gap_types = [g.gap_type for g in gaps]
        assert "low_confidence_hub" in gap_types

    def test_orphan_entity_detected(self):
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        hops = [RetrievalHop(
            entity_id="e1", entity_name="Orphan", entity_type="system",
            layer="structural", confidence=0.9, hop_number=0,
            matched_by="keyword", fused_score=0.5,
            gap_flag=True, gap_reason="orphan_entity",
        )]

        gaps = pipeline._stage7_gaps(hops, AnswerScore.PARTIAL, "test question")
        gap_types = [g.gap_type for g in gaps]
        assert "orphan_entity" in gap_types

    def test_not_answerable_thin_coverage(self):
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        hops = [RetrievalHop(
            entity_id="e1", entity_name="Something", entity_type="system",
            layer="structural", confidence=0.9, hop_number=0,
            matched_by="keyword", fused_score=0.5,
        )]

        gaps = pipeline._stage7_gaps(hops, AnswerScore.NOT_ANSWERABLE, "test question")
        gap_types = [g.gap_type for g in gaps]
        assert "thin_coverage" in gap_types

    def test_not_answerable_missing_entity(self):
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        gaps = pipeline._stage7_gaps([], AnswerScore.NOT_ANSWERABLE, "test question")
        gap_types = [g.gap_type for g in gaps]
        assert "missing_entity" in gap_types

    def test_ambiguous_entity_detected(self):
        from context_blocks.retrieval.pipeline import RetrievalPipeline
        from unittest.mock import MagicMock

        backend = MagicMock()
        pipeline = RetrievalPipeline(backend)

        hops = [
            RetrievalHop(
                entity_id="e1", entity_name="Fraud Detection", entity_type="system",
                layer="structural", confidence=0.9, hop_number=0,
                matched_by="keyword", fused_score=0.8,
            ),
            RetrievalHop(
                entity_id="e2", entity_name="Fraud Detection Team", entity_type="team",
                layer="organizational", confidence=0.9, hop_number=0,
                matched_by="keyword", fused_score=0.8,
            ),
        ]

        gaps = pipeline._stage7_gaps(hops, AnswerScore.PARTIAL, "test question")
        gap_types = [g.gap_type for g in gaps]
        assert "ambiguous_entity" in gap_types
