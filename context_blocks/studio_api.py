"""Context Blocks Studio API — block authoring/management over HTTP.

Distinct from ``context_blocks.api`` (which serves *one* block's retrieval KB
loaded at startup). The Studio API is **block-aware**: it operates on the
project's block registry and can create/list/inspect *any* block. It wraps the
same engine primitives the CLI uses (``BlockRegistry.create``), so a block
created via the API is identical to one created via ``cb init``.

Run:
    uvicorn context_blocks.studio_api:create_studio_app --factory --port 8322
    # project root: --root arg, or CB_PROJECT_ROOT env, or auto-discovered
"""

from __future__ import annotations

import os
from pathlib import Path

import structlog
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from context_blocks.blocks import (
    BlockConfig,
    BlockRegistry,
    find_project_root,
    is_valid_block_name,
)
from context_blocks.ontology import Ontology, load_ontology_from_file

logger = structlog.get_logger(__name__)

# Conventional filenames written into a block directory.
META_MODEL_FILENAME = "meta-model.yaml"
SEED_FILENAME = "seed-context.md"
PROJECT_MARKER = ".contextblocks"


# ── Request / Response models ──

class CreateBlockRequest(BaseModel):
    name: str
    description: str = ""
    label: str = ""
    model: str = ""
    # "default" (built-in meta-model) or a path string already on disk.
    ontology: str = "default"
    # Optional inline meta-model YAML — written into the block as meta-model.yaml
    # and referenced by the block (takes precedence over `ontology`).
    ontology_yaml: str | None = None
    # Optional inline seed-context markdown — written into the block.
    seed_context: str | None = None


class OntologySummary(BaseModel):
    source: str
    types: list[str]
    layers: list[str]
    relationship_field_count: int


class BlockSummary(BaseModel):
    name: str
    description: str
    label: str
    ontology: str
    output: str
    seed_context: str
    model: str
    entity_count: int
    created_at: str
    last_updated: str
    output_dir: str


class BlockDetail(BlockSummary):
    ontology_detail: OntologySummary


# ── Helpers ──

def _resolve_root(root: str | Path | None) -> Path:
    """Resolve the project root: explicit arg, CB_PROJECT_ROOT env, or discovery."""
    if root:
        return Path(root)
    env_root = os.environ.get("CB_PROJECT_ROOT")
    if env_root:
        return Path(env_root)
    return find_project_root()


def _resolve_ontology(root: Path, config: BlockConfig) -> Ontology:
    """Load the block's ontology (custom file relative to root, or built-in default)."""
    onto = config.ontology or "default"
    if onto == "default":
        return Ontology()
    for candidate in (root / onto, Path(onto)):
        if candidate.exists():
            try:
                return load_ontology_from_file(candidate)
            except Exception as e:  # noqa: BLE001 — fall back to default on any parse error
                logger.warning("studio_ontology_load_failed", path=str(candidate), error=str(e))
                return Ontology()
    return Ontology()


def _ontology_summary(ont: Ontology) -> OntologySummary:
    return OntologySummary(
        source=ont.source,
        types=sorted(ont.types),
        layers=sorted(set(ont.type_to_layer.values())),
        relationship_field_count=len(ont.relationship_fields),
    )


def _summary(reg: BlockRegistry, config: BlockConfig) -> BlockSummary:
    return BlockSummary(
        name=config.name,
        description=config.description,
        label=config.label,
        ontology=config.ontology,
        output=config.output,
        seed_context=config.seed_context,
        model=config.model,
        entity_count=config.entity_count,
        created_at=config.created_at,
        last_updated=config.last_updated,
        output_dir=str(reg.block_output_dir(config.name)),
    )


# ── App factory ──

def create_studio_app(root: str | Path | None = None) -> FastAPI:
    """Create the Studio FastAPI app bound to a project root's block registry."""
    project_root = _resolve_root(root)

    app = FastAPI(
        title="Context Blocks Studio API",
        description="Author and manage context blocks",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def registry() -> BlockRegistry:
        # Re-read the registry per request so external edits are picked up.
        return BlockRegistry(project_root)

    @app.get("/health")
    async def health() -> dict:
        reg = registry()
        return {"status": "ok", "root": str(project_root), "blocks": len(reg.list_blocks())}

    @app.get("/blocks", response_model=list[BlockSummary])
    async def list_blocks() -> list[BlockSummary]:
        reg = registry()
        return [_summary(reg, cfg) for cfg in reg.list_blocks()]

    @app.get("/blocks/{name}", response_model=BlockDetail)
    async def get_block(name: str) -> BlockDetail:
        reg = registry()
        config = reg.get(name)
        if config is None:
            raise HTTPException(status_code=404, detail=f"Block '{name}' not found")
        ont = _resolve_ontology(project_root, config)
        base = _summary(reg, config)
        return BlockDetail(**base.model_dump(), ontology_detail=_ontology_summary(ont))

    @app.post("/blocks", response_model=BlockDetail, status_code=201)
    async def create_block(req: CreateBlockRequest) -> BlockDetail:
        reg = registry()

        if not is_valid_block_name(req.name):
            raise HTTPException(
                status_code=422,
                detail=f"Invalid block name '{req.name}'. Use kebab-case (e.g. 'payments', 'cost-control').",
            )
        if reg.exists(req.name):
            raise HTTPException(status_code=409, detail=f"Block '{req.name}' already exists")

        # Resolve ontology: inline YAML takes precedence and is written into the block.
        ontology_ref = req.ontology
        if req.ontology_yaml is not None:
            try:
                parsed = yaml.safe_load(req.ontology_yaml)
            except yaml.YAMLError as e:
                raise HTTPException(status_code=422, detail=f"Ontology YAML is not valid: {e}") from None
            if not isinstance(parsed, dict):
                raise HTTPException(status_code=422, detail="Ontology YAML must be a mapping")
            ontology_ref = f"{req.name}/{META_MODEL_FILENAME}"

        seed_ref = ""
        if req.seed_context is not None:
            seed_ref = f"{req.name}/{SEED_FILENAME}"

        config = BlockConfig(
            name=req.name,
            description=req.description,
            label=req.label,
            ontology=ontology_ref,
            seed_context=seed_ref,
            model=req.model,
        )

        block_dir = reg.create(config)

        # Write inline artifacts after the block dir exists.
        if req.ontology_yaml is not None:
            (block_dir / META_MODEL_FILENAME).write_text(req.ontology_yaml, encoding="utf-8")
        if req.seed_context is not None:
            (block_dir / SEED_FILENAME).write_text(req.seed_context, encoding="utf-8")

        marker = project_root / PROJECT_MARKER
        if not marker.exists():
            marker.write_text("# Context Blocks project root\n", encoding="utf-8")

        logger.info("studio_block_created", name=req.name, dir=str(block_dir))

        ont = _resolve_ontology(project_root, config)
        base = _summary(reg, config)
        return BlockDetail(**base.model_dump(), ontology_detail=_ontology_summary(ont))

    return app
