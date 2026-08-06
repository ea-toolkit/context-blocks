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
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from context_blocks import storage
from context_blocks.blocks import (
    BlockConfig,
    BlockRegistry,
    find_project_root,
    is_valid_block_name,
)
from context_blocks.meta_model import get_directory_for_type
from context_blocks.ontology import Ontology, load_ontology_from_file
from context_blocks.validation import parse_frontmatter, validate_entity_frontmatter

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


class AddEntityRequest(BaseModel):
    # Full entity markdown: YAML frontmatter + body.
    content: str
    # Optional expected id; when given, the frontmatter id must match it.
    id: str | None = None


class AddEntityResponse(BaseModel):
    id: str
    type: str
    # Path of the written file, relative to the block's output dir.
    path: str
    # Non-blocking notes (e.g. custom-metadata fields kept but not graphed).
    warnings: list[str] = []


class EntityListItem(BaseModel):
    id: str
    type: str
    name: str
    # Path of the entity file, relative to the block's output dir.
    path: str


class ArtifactInfoResponse(BaseModel):
    filename: str
    path: str
    size: int
    content_type: str


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
    """Create the Studio FastAPI app bound to a project root's block registry.

    Serves JSON only — the authoring UI lives in the Astro viewer (viewer/) and
    calls this API via PUBLIC_CB_STUDIO_API_BASE.
    """
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

    @app.get("/blocks/{name}/entities", response_model=list[EntityListItem])
    async def list_entities(name: str) -> list[EntityListItem]:
        reg = registry()
        config = reg.get(name)
        if config is None:
            raise HTTPException(status_code=404, detail=f"Block '{name}' not found")

        output_dir = reg.block_output_dir(name)
        entities_dir = output_dir / "entities"
        items: list[EntityListItem] = []
        if entities_dir.exists():
            for md in sorted(entities_dir.rglob("*.md")):
                fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
                if not fm:
                    continue
                items.append(
                    EntityListItem(
                        id=str(fm.get("id", md.stem)),
                        type=str(fm.get("type", "")),
                        name=str(fm.get("name", fm.get("id", md.stem))),
                        path=str(md.relative_to(output_dir)),
                    )
                )
        return items

    @app.post("/blocks/{name}/entities", response_model=AddEntityResponse, status_code=201)
    async def add_entity(name: str, req: AddEntityRequest) -> AddEntityResponse:
        reg = registry()
        config = reg.get(name)
        if config is None:
            raise HTTPException(status_code=404, detail=f"Block '{name}' not found")

        ont = _resolve_ontology(project_root, config)
        result = validate_entity_frontmatter(req.content, ont, expected_id=req.id)
        if not result.valid:
            raise HTTPException(status_code=422, detail={"errors": result.error_messages})

        entity_type = str(result.frontmatter["type"])
        entity_id = str(result.frontmatter["id"])
        directory = get_directory_for_type(entity_type, ontology=ont)

        output_dir = reg.block_output_dir(name)
        dest_dir = output_dir / "entities" / directory
        dest = dest_dir / f"{entity_id}.md"
        if dest.exists():
            raise HTTPException(
                status_code=409,
                detail=f"Entity '{entity_id}' already exists in block '{name}'",
            )

        dest_dir.mkdir(parents=True, exist_ok=True)
        dest.write_text(req.content, encoding="utf-8")

        logger.info("studio_entity_added", block=name, entity_id=entity_id, type=entity_type)
        return AddEntityResponse(
            id=entity_id,
            type=entity_type,
            path=str(dest.relative_to(output_dir)),
            warnings=result.warning_messages,
        )

    def _require_block(name: str) -> None:
        if registry().get(name) is None:
            raise HTTPException(status_code=404, detail=f"Block '{name}' not found")

    def _artifact_response(info: storage.ArtifactInfo) -> ArtifactInfoResponse:
        return ArtifactInfoResponse(
            filename=info.filename, path=info.path, size=info.size, content_type=info.content_type
        )

    @app.post("/blocks/{name}/artifacts", response_model=ArtifactInfoResponse, status_code=201)
    async def upload_artifact(name: str, file: UploadFile = File(...)) -> ArtifactInfoResponse:
        _require_block(name)
        filename = file.filename or ""
        if not storage.is_allowed_artifact(filename):
            allowed = ", ".join(sorted(storage.ARTIFACT_EXTENSIONS))
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported artifact type '{filename}'. Allowed: {allowed}",
            )
        data = await file.read()
        info = storage.save_artifact(registry().block_output_dir(name), filename, data)
        logger.info("studio_artifact_uploaded", block=name, filename=info.filename, size=info.size)
        return _artifact_response(info)

    @app.get("/blocks/{name}/artifacts", response_model=list[ArtifactInfoResponse])
    async def list_block_artifacts(name: str) -> list[ArtifactInfoResponse]:
        _require_block(name)
        return [_artifact_response(a) for a in storage.list_artifacts(registry().block_output_dir(name))]

    @app.get("/blocks/{name}/artifacts/{filename}")
    async def get_artifact(name: str, filename: str) -> Response:
        _require_block(name)
        result = storage.read_artifact(registry().block_output_dir(name), filename)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Artifact '{filename}' not found")
        data, content_type = result
        return Response(content=data, media_type=content_type)

    return app
