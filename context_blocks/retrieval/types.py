"""Data types for the retrieval pipeline."""
from dataclasses import dataclass, field
from enum import Enum


class AnswerScore(str, Enum):
    ANSWERABLE = "answerable"
    PARTIAL = "partial"
    NOT_ANSWERABLE = "not_answerable"


@dataclass
class QueryUnderstanding:
    """Output of Stage 0: intent classification + retrieval parameters."""
    original_question: str
    intent_weights: dict[str, float] = field(default_factory=dict)
    layer_priorities: dict[str, float] = field(default_factory=dict)
    edge_priorities: list[str] | None = None  # None = follow all edges
    keywords: list[str] = field(default_factory=list)
    is_listing_query: bool = False
    is_comparison_query: bool = False


@dataclass
class ScoredEntity:
    """An entity with its retrieval score and metadata."""
    entity_id: str
    name: str
    entity_type: str
    layer: str
    confidence: float
    description: str
    overview: str
    body: str
    relationships: list[dict]  # [{type, target_id}]
    source_documents: list[str]
    score: float = 0.0
    matched_by: str = ""  # 'vector' | 'keyword' | 'graph'
    hop_number: int = 0
    hop_decay: float = 1.0
    relationship_from: str | None = None
    relationship_type: str | None = None
    # Multi-method provenance: preserved even when a higher-scoring method wins
    found_by: list[str] | None = None  # all methods that found this entity
    graph_hop: int | None = None  # graph hop number (preserved separately)
    graph_from: str | None = None  # graph relationship source entity
    graph_rel: str | None = None  # graph relationship type


@dataclass
class RetrievalHop:
    """A single hop in the retrieval trace."""
    entity_id: str
    entity_name: str
    entity_type: str
    layer: str
    confidence: float
    hop_number: int
    matched_by: str
    relationship_from: str | None = None
    relationship_type: str | None = None
    fused_score: float = 0.0
    gap_flag: bool = False
    gap_reason: str | None = None
    found_by: list[str] | None = None  # all methods: ['keyword', 'graph']


@dataclass
class Gap:
    """A knowledge gap detected during retrieval."""
    gap_type: str  # missing_entity | thin_coverage | low_confidence_hub | broken_relationship | orphan_entity | ambiguous_entity
    entity_id: str | None
    description: str
    suggested_action: str
    severity: str  # high | medium | low
    source_question: str


@dataclass
class StageTrace:
    """Detailed per-stage trace for debugging the retrieval funnel."""
    intent_weights: dict[str, float] = field(default_factory=dict)
    layer_priorities: dict[str, float] = field(default_factory=dict)
    vector_candidates: int = 0
    keyword_candidates: int = 0
    graph_candidates: int = 0
    fused_unique: int = 0
    after_scoring: int = 0
    after_dedup: int = 0
    context_selected: int = 0
    tokens_used: int = 0
    token_budget: int = 0
    synthesis_score: str = ""
    gaps_detected: int = 0


@dataclass
class RetrievalTrace:
    """Complete trace of one retrieval operation."""
    question: str
    sub_queries: list[str]
    intent_weights: dict[str, float]
    hops: list[RetrievalHop] = field(default_factory=list)
    stage_trace: StageTrace | None = None
    total_entities_searched: int = 0
    total_entities_retrieved: int = 0
    vector_search_ms: int = 0
    keyword_search_ms: int = 0
    graph_search_ms: int = 0
    synthesis_ms: int = 0
    total_ms: int = 0
    tokens_used: int = 0
    gaps: list[Gap] = field(default_factory=list)


@dataclass
class RetrievalResult:
    """Complete output of the retrieval pipeline."""
    answer: str
    citations: list[str]
    score: AnswerScore
    trace: RetrievalTrace
    gaps: list[Gap]
    context_text: str = ""  # the assembled context sent to LLM
