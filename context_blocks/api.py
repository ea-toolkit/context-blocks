"""Context Blocks API — FastAPI server for live retrieval queries.

Loads the KB once on startup, serves queries via HTTP.
The viewer calls this for the Ask page live experience.

Usage:
    context-blocks serve --output <dir> [--port 8321]
    # or directly:
    uvicorn context_blocks.api:create_app --factory --port 8321
"""
import os
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


# ── Request/Response Models ──

class AskRequest(BaseModel):
    question: str
    debug: bool = False
    full_trace: bool = False


class HopResponse(BaseModel):
    hop_number: int
    entity_id: str
    entity_name: str
    entity_type: str
    layer: str
    matched_by: str
    confidence: float
    fused_score: float
    relationship_from: str | None = None
    relationship_type: str | None = None
    gap_flag: bool = False
    gap_reason: str | None = None
    found_by: list[str] | None = None


class GapResponse(BaseModel):
    gap_type: str
    entity_id: str | None = None
    description: str
    suggested_action: str
    severity: str


class StageTraceResponse(BaseModel):
    vector_candidates: int
    keyword_candidates: int
    graph_candidates: int
    fused_unique: int
    after_dedup: int
    context_selected: int
    tokens_used: int
    token_budget: int
    intent_weights: dict[str, float] | None = None
    layer_priorities: dict[str, float] | None = None
    search_ms: int | None = None
    synthesis_ms: int | None = None


class AskResponse(BaseModel):
    answer: str
    score: str
    ddc_class: str
    citations: list[str]
    hops: list[HopResponse]
    gaps: list[GapResponse]
    stage_trace: StageTraceResponse | None = None
    entities_retrieved: int
    total_ms: int


class StatsResponse(BaseModel):
    entity_count: int
    edge_count: int
    document_count: int


# ── App Factory ──

def create_app(
    output_dir: str | None = None,
    provider: str = "anthropic",
    embedder: str = "auto",
) -> FastAPI:
    """Create the FastAPI app with KB loaded."""
    from dotenv import load_dotenv
    load_dotenv()

    from context_blocks.retrieval.backend import InMemoryBackend
    from context_blocks.retrieval.embedder import get_embedder, index_entities
    from context_blocks.retrieval.pipeline import RetrievalPipeline
    from context_blocks.retrieval.synthesis import get_synthesizer
    from context_blocks.retrieval.types import AnswerScore

    output_path = Path(output_dir or os.environ.get("CB_OUTPUT_DIR", "output"))
    entity_dir = output_path / "entities"

    app = FastAPI(
        title="Context Blocks API",
        description="Live retrieval queries against your domain knowledge base",
        version="0.1.0",
    )

    # CORS for viewer (localhost dev + any origin for now)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # State — loaded once on startup
    state: dict = {}

    @app.on_event("startup")
    async def startup():
        logger.info("api_starting", entity_dir=str(entity_dir))

        if not entity_dir.exists():
            logger.error("entity_dir_not_found", path=str(entity_dir))
            return

        # Load backend
        backend = InMemoryBackend()
        backend.load_from_entity_dir(entity_dir)
        logger.info("backend_loaded", entities=backend.entity_count())

        # Embed entities
        openai_key = os.environ.get("OPENAI_API_KEY")
        emb = get_embedder(provider=embedder, api_key=openai_key)
        count = await index_entities(backend, emb)
        logger.info("embeddings_indexed", count=count)

        # Set up synthesizer
        llm_key = os.environ.get("LLM_API_KEY", "")
        synth = get_synthesizer(provider=provider, api_key=llm_key)

        # Build pipeline
        pipeline = RetrievalPipeline(backend, embed_fn=emb.embed, synthesize_fn=synth)

        # Count source docs
        doc_count = 0
        docs_dir = output_path.parent / "docs"
        if docs_dir.exists():
            doc_count = len(list(docs_dir.glob("**/*.txt")) + list(docs_dir.glob("**/*.md")))

        state["backend"] = backend
        state["pipeline"] = pipeline
        state["doc_count"] = doc_count
        logger.info("api_ready", entities=backend.entity_count(), docs=doc_count)

    @app.get("/stats", response_model=StatsResponse)
    async def get_stats():
        backend = state.get("backend")
        if not backend:
            return StatsResponse(entity_count=0, edge_count=0, document_count=0)
        return StatsResponse(
            entity_count=backend.entity_count(),
            edge_count=sum(len(v) for v in backend.graph.values()),
            document_count=state.get("doc_count", 0),
        )

    @app.post("/ask", response_model=AskResponse)
    async def ask(req: AskRequest):
        pipeline = state.get("pipeline")
        if not pipeline:
            return AskResponse(
                answer="KB not loaded. Check server logs.",
                score="not_answerable", ddc_class="MISSING",
                citations=[], hops=[], gaps=[],
                entities_retrieved=0, total_ms=0,
            )

        ddc_map = {
            AnswerScore.ANSWERABLE: "CLEAN",
            AnswerScore.PARTIAL: "INCOMPLETE",
            AnswerScore.NOT_ANSWERABLE: "MISSING",
        }

        result = await pipeline.retrieve(req.question, debug=req.debug, full_trace=req.full_trace)

        hops = [
            HopResponse(
                hop_number=h.hop_number,
                entity_id=h.entity_id,
                entity_name=h.entity_name,
                entity_type=h.entity_type,
                layer=h.layer,
                matched_by=h.matched_by,
                confidence=h.confidence,
                fused_score=h.fused_score,
                relationship_from=h.relationship_from,
                relationship_type=h.relationship_type,
                gap_flag=h.gap_flag,
                gap_reason=h.gap_reason,
                found_by=h.found_by,
            )
            for h in result.trace.hops
        ]

        gaps = [
            GapResponse(
                gap_type=g.gap_type,
                entity_id=g.entity_id,
                description=g.description,
                suggested_action=g.suggested_action,
                severity=g.severity,
            )
            for g in result.gaps
        ]

        stage_trace = None
        if result.trace.stage_trace:
            st = result.trace.stage_trace
            stage_trace = StageTraceResponse(
                vector_candidates=st.vector_candidates,
                keyword_candidates=st.keyword_candidates,
                graph_candidates=st.graph_candidates,
                fused_unique=st.fused_unique,
                after_dedup=st.after_dedup,
                context_selected=st.context_selected,
                tokens_used=st.tokens_used,
                token_budget=st.token_budget,
                intent_weights=st.intent_weights if st.intent_weights else None,
                layer_priorities=st.layer_priorities if st.layer_priorities else None,
                search_ms=result.trace.vector_search_ms if result.trace.vector_search_ms else None,
                synthesis_ms=result.trace.synthesis_ms if result.trace.synthesis_ms else None,
            )

        return AskResponse(
            answer=result.answer,
            score=result.score.value,
            ddc_class=ddc_map.get(result.score, "MISSING"),
            citations=result.citations,
            hops=hops,
            gaps=gaps,
            stage_trace=stage_trace,
            entities_retrieved=result.trace.total_entities_retrieved,
            total_ms=result.trace.total_ms,
        )

    @app.get("/health")
    async def health():
        backend = state.get("backend")
        return {
            "status": "ok" if backend else "no_kb",
            "entities": backend.entity_count() if backend else 0,
        }

    return app
