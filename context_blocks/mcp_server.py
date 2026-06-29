"""Context Blocks MCP Server — expose KB to AI agents via Model Context Protocol.

6 read-only tools for agents to query knowledge bases:
- list_blocks: discover available context blocks (domains)
- get_overview: KB stats and structure for a block
- search_entities: find entities by text query
- get_entity: full detail for one entity
- ask_kb: full DAR retrieval pipeline (requires API keys)
- get_gap_report: coverage gaps, optionally per persona

Block-aware: agents discover blocks via list_blocks(), then pass the block
name to any tool. If only one block exists, it's used by default.

Usage:
    cb mcp                        # serve all blocks in project
    cb mcp --block my-domain      # serve a single block (legacy)
    cb mcp --output path/to/output # serve a direct output directory
"""
import asyncio
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Context Blocks",
    instructions="Query domain knowledge bases built by Context Blocks. "
    "Start with list_blocks() to see available domains, then use the block name "
    "in other tools. If there's only one block, it's used automatically.",
)

_block_cache: dict[str, dict] = {}
_project_root: Path = Path.cwd()
_single_output: str = ""

LAYER_MAP = {
    "system": "Structural", "software-component": "Structural",
    "api": "Structural", "data-model": "Structural",
    "data-product": "Structural", "platform": "Structural",
    "process": "Behavioral", "business-event": "Behavioral",
    "domain-logic": "Behavioral",
    "reference-data": "Reference",
    "team": "Organizational", "persona": "Organizational",
    "capability": "Organizational", "offering": "Organizational",
    "external-party": "Organizational",
    "jargon-business": "Language", "jargon-tech": "Language",
    "decision": "Decision",
}


def _parse_frontmatter(raw: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?\n)---\n?(.*)", raw, re.DOTALL)
    if not match:
        return {}, raw
    try:
        fm = yaml.safe_load(match.group(1))
        return (fm if isinstance(fm, dict) else {}), match.group(2)
    except yaml.YAMLError:
        return {}, raw


def _load_entities(entity_dir: Path) -> list[dict]:
    entities = []
    for type_dir in sorted(entity_dir.iterdir()):
        if not type_dir.is_dir():
            continue
        for filepath in sorted(type_dir.glob("*.md")):
            raw = filepath.read_text(encoding="utf-8")
            fm, body = _parse_frontmatter(raw)
            if not fm:
                continue
            eid = fm.get("id", filepath.stem)
            etype = fm.get("type", type_dir.name)
            entities.append({
                "id": eid,
                "name": fm.get("name", eid),
                "type": etype,
                "layer": LAYER_MAP.get(etype, "Other"),
                "description": fm.get("description", ""),
                "status": fm.get("status", "active"),
                "confidence": fm.get("confidence", 1.0),
                "relationships": _extract_rels(fm),
                "source_documents": fm.get("source_documents", []),
                "body": body.strip(),
                "file": str(filepath),
            })
    return entities


REL_FIELDS = [
    "related_to", "depends_on", "owned_by", "deployed_on",
    "implements_capability", "consumes", "produces", "triggers",
    "triggered_by", "affects", "affected_by", "related_systems",
    "related_processes", "triggered", "published_by", "subscribed_by",
    "managed_by",
]


def _extract_rels(fm: dict) -> list[dict]:
    rels = []
    for field in REL_FIELDS:
        refs = fm.get(field)
        if not refs:
            continue
        if isinstance(refs, str):
            refs = [refs]
        for ref in refs:
            rels.append({"type": field, "target_id": ref})
    return rels


def _get_available_blocks() -> list[dict]:
    """Discover blocks from registry or single output dir."""
    if _single_output:
        output_dir = Path(_single_output)
        entity_dir = output_dir / "entities"
        name = output_dir.parent.name if output_dir.name == "output" else output_dir.name
        return [{"name": name, "output_dir": str(output_dir), "has_entities": entity_dir.exists()}]

    registry_path = _project_root / "blocks.yaml"
    if registry_path.exists():
        raw = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            blocks = []
            for name, cfg in raw.items():
                block_dir = _project_root / name
                entity_dir = block_dir / "entities"
                blocks.append({
                    "name": name,
                    "description": cfg.get("description", ""),
                    "entity_count": cfg.get("entity_count", 0),
                    "output_dir": str(block_dir),
                    "has_entities": entity_dir.exists(),
                })
            return blocks

    output_dir = Path(os.environ.get("CB_OUTPUT_DIR", "output"))
    entity_dir = output_dir / "entities"
    if entity_dir.exists():
        return [{"name": "default", "output_dir": str(output_dir), "has_entities": True}]

    return []


def _resolve_block(block: str) -> dict:
    """Resolve a block name to its cached data. Loads entities on first access."""
    available = _get_available_blocks()

    if not available:
        return {"error": "No blocks found. Run cb init or cb phase1 first."}

    if not block:
        if len(available) == 1:
            block = available[0]["name"]
        else:
            names = [b["name"] for b in available]
            return {"error": f"Multiple blocks available: {names}. Specify a block name."}

    target = None
    for b in available:
        if b["name"] == block:
            target = b
            break

    if not target:
        names = [b["name"] for b in available]
        return {"error": f"Block '{block}' not found. Available: {names}"}

    if block not in _block_cache:
        output_dir = Path(target["output_dir"])
        entity_dir = output_dir / "entities"
        if not entity_dir.exists():
            _block_cache[block] = {
                "entities": [], "entity_index": {}, "output_dir": output_dir, "name": block,
            }
        else:
            entities = _load_entities(entity_dir)
            _block_cache[block] = {
                "entities": entities,
                "entity_index": {e["id"]: e for e in entities},
                "output_dir": output_dir,
                "name": block,
            }

    return _block_cache[block]


@mcp.tool()
def list_blocks() -> list[dict]:
    """List all available context blocks (domains). Call this first to discover what knowledge bases are available. Each block is an independent domain with its own entities, relationships, and evaluations. Returns a list of blocks with: name, description, entity_count, and whether entities have been extracted. Pass the block name to other tools to query a specific domain."""
    available = _get_available_blocks()
    if not available:
        return [{"message": "No blocks found. Run cb init or cb phase1 first."}]

    results = []
    for b in available:
        entry = {"name": b["name"], "has_entities": b["has_entities"]}
        if b.get("description"):
            entry["description"] = b["description"]
        if b.get("entity_count"):
            entry["entity_count"] = b["entity_count"]
        results.append(entry)
    return results


@mcp.tool()
def get_overview(block: str = "") -> dict:
    """Use this when starting a conversation about a domain. Returns the KB structure for a block: total entity count, entities per type (system, process, team, etc.), entities per knowledge layer (Structural, Behavioral, Organizational, Language, Decision, Reference), total relationships, and average confidence score. Pass block name from list_blocks(). If only one block exists, it's used automatically. Returns a dict with keys: block, total_entities, total_relationships, average_confidence, entities_by_type, entities_by_layer, entity_types, layers."""
    data = _resolve_block(block)
    if "error" in data:
        return data

    entities = data.get("entities", [])
    type_counts = Counter(e["type"] for e in entities)
    layer_counts = Counter(e["layer"] for e in entities)
    total_rels = sum(len(e["relationships"]) for e in entities)
    avg_confidence = (
        sum(e["confidence"] for e in entities) / len(entities)
        if entities else 0
    )

    return {
        "block": data["name"],
        "total_entities": len(entities),
        "total_relationships": total_rels,
        "average_confidence": round(avg_confidence, 3),
        "entities_by_type": dict(type_counts.most_common()),
        "entities_by_layer": dict(layer_counts.most_common()),
        "entity_types": sorted(type_counts.keys()),
        "layers": sorted(layer_counts.keys()),
    }


@mcp.tool()
def search_entities(
    query: str,
    block: str = "",
    entity_type: str = "",
    layer: str = "",
    limit: int = 10,
) -> list[dict]:
    """Find entities matching a text query within a block. Use when you need to discover what the KB knows about a topic — e.g. 'claims routing', 'authentication', 'payment processing'. Pass block name from list_blocks(). Filter by entity_type (system, process, api, data-model, team, persona, capability, business-event, domain-logic, jargon-business, jargon-tech, etc.) or layer (Structural, Behavioral, Organizational, Language, Decision, Reference). Returns up to `limit` results sorted by relevance, each with: id, name, type, layer, confidence, description, and top 5 relationships. Use get_entity() with the returned id for full detail."""
    data = _resolve_block(block)
    if "error" in data:
        return [data]

    entities = data.get("entities", [])
    block_name = data["name"]

    query_terms = set(re.findall(r"\w+", query.lower()))
    if not query_terms:
        return []

    scored = []
    for e in entities:
        if entity_type and e["type"] != entity_type:
            continue
        if layer and e["layer"] != layer:
            continue

        name_terms = set(re.findall(r"\w+", e["name"].lower()))
        desc_terms = set(re.findall(r"\w+", e["description"].lower()))
        body_terms = set(re.findall(r"\w+", e["body"][:500].lower()))

        name_hits = len(query_terms & name_terms) * 3
        desc_hits = len(query_terms & desc_terms) * 2
        body_hits = len(query_terms & body_terms)
        score = name_hits + desc_hits + body_hits

        if score > 0:
            scored.append((score, e))

    scored.sort(key=lambda x: -x[0])

    return [
        {
            "id": e["id"],
            "name": e["name"],
            "type": e["type"],
            "layer": e["layer"],
            "confidence": e["confidence"],
            "description": e["description"],
            "relationships": e["relationships"][:5],
            "relevance_score": s,
            "block": block_name,
        }
        for s, e in scored[:limit]
    ]


@mcp.tool()
def get_entity(entity_id: str, block: str = "") -> dict:
    """Get the complete detail for one entity. Use after search_entities() returns an id you want to explore, or when you already know the entity id (kebab-case, e.g. 'claims-gateway', 'claim-routing-process'). Pass block name from list_blocks() or omit for single-block projects. Returns: id, name, type, layer, status, confidence score (0-1), description, full markdown body, all relationships (type + target_id), and source documents that created this entity. Returns {error: '...'} if the id doesn't exist."""
    data = _resolve_block(block)
    if "error" in data:
        return data

    index = data.get("entity_index", {})
    e = index.get(entity_id)
    if not e:
        return {"error": f"Entity '{entity_id}' not found in block '{data['name']}'"}

    return {
        "id": e["id"],
        "name": e["name"],
        "type": e["type"],
        "layer": e["layer"],
        "status": e["status"],
        "confidence": e["confidence"],
        "description": e["description"],
        "body": e["body"],
        "relationships": e["relationships"],
        "source_documents": e["source_documents"],
        "block": data["name"],
    }


@mcp.tool()
def ask_kb(question: str, block: str = "") -> dict:
    """Ask a natural language question and get a grounded answer from a block's KB. This runs the full Domain-Aware Retrieval (DAR) pipeline: intent classification, parallel search (vector + keyword + graph), RRF fusion, LLM synthesis, and gap detection. Use for complex questions like 'How does claim routing work?', 'What systems depend on the claims gateway?', 'Who owns the payment processing flow?'. Pass block name from list_blocks(). Returns: answer (grounded text), ddc_class (CLEAN = fully answerable, INCOMPLETE = partial, MISSING = not answerable), citations (entity ids used), entities_retrieved count, gaps (knowledge gaps detected with suggested actions), and total_ms. Requires LLM_API_KEY env var. First call per block is slow (~5s) as it loads embeddings; subsequent calls are fast."""
    data = _resolve_block(block)
    if "error" in data:
        return data

    output_dir = data["output_dir"]
    entity_dir = output_dir / "entities"
    block_name = data["name"]
    cache_key = f"pipeline_{block_name}"

    if not entity_dir.exists():
        return {"error": f"No entities found in block '{block_name}'. Run cb phase1 first."}

    llm_key = os.environ.get("LLM_API_KEY", "")
    if not llm_key:
        return {"error": "LLM_API_KEY not set. Required for ask_kb."}

    from context_blocks.retrieval.backend import InMemoryBackend
    from context_blocks.retrieval.embedder import get_embedder, index_entities
    from context_blocks.retrieval.pipeline import RetrievalPipeline
    from context_blocks.retrieval.synthesis import get_synthesizer

    if cache_key not in _block_cache:
        backend = InMemoryBackend()
        backend.load_from_entity_dir(entity_dir)

        openai_key = os.environ.get("OPENAI_API_KEY")
        emb = get_embedder(provider="auto", api_key=openai_key)
        asyncio.get_event_loop().run_until_complete(index_entities(backend, emb))

        synth = get_synthesizer(provider="anthropic", api_key=llm_key)
        pipeline = RetrievalPipeline(backend, embed_fn=emb.embed, synthesize_fn=synth)

        _block_cache[cache_key] = {"pipeline": pipeline}

    pipeline = _block_cache[cache_key]["pipeline"]
    result = asyncio.get_event_loop().run_until_complete(
        pipeline.retrieve(question)
    )

    ddc_map = {"answerable": "CLEAN", "partial": "INCOMPLETE", "not_answerable": "MISSING"}

    return {
        "block": block_name,
        "answer": result.answer,
        "ddc_class": ddc_map.get(result.score.value, "MISSING"),
        "citations": result.citations,
        "entities_retrieved": result.trace.total_entities_retrieved,
        "gaps": [
            {
                "type": g.gap_type,
                "description": g.description,
                "suggested_action": g.suggested_action,
                "severity": g.severity,
            }
            for g in result.gaps
        ],
        "total_ms": result.trace.total_ms,
    }


@mcp.tool()
def get_gap_report(block: str = "", persona: str = "") -> dict:
    """Get knowledge coverage gaps from the most recent cb eval run for a block. Use when someone asks 'What's missing from the KB?', 'How complete is the documentation?', or 'What does a new developer need that isn't documented?'. Pass block name from list_blocks(). Filter by persona to get role-specific gaps (developer, architect, product-owner, new-joiner). Returns: total_questions evaluated, coverage breakdown (CLEAN/INCOMPLETE/MISSING counts), gap_count, and up to 20 gap details each with the question, ddc_class, source persona, and detected gaps. Returns {error: '...'} if cb eval hasn't been run yet."""
    data = _resolve_block(block)
    if "error" in data:
        return data

    output_dir = data["output_dir"]
    block_name = data["name"]

    eval_dir = output_dir / "evals"
    if not eval_dir.exists():
        return {"error": f"No eval results found for block '{block_name}'. Run cb eval first."}

    latest_run = None
    for d in sorted(eval_dir.iterdir(), reverse=True):
        if d.is_dir() and (d / "results.yaml").exists():
            latest_run = d
            break

    if not latest_run:
        report_file = eval_dir / "report.yaml"
        if not report_file.exists():
            return {"error": f"No eval report found for block '{block_name}'. Run cb eval first."}
        report = yaml.safe_load(report_file.read_text(encoding="utf-8"))
    else:
        report = yaml.safe_load(
            (latest_run / "results.yaml").read_text(encoding="utf-8")
        )

    if not isinstance(report, dict):
        return {"error": "Could not parse eval report"}

    questions = report.get("questions", report.get("results", []))
    if not isinstance(questions, list):
        return {"error": "Unexpected eval report format"}

    if persona:
        questions = [
            q for q in questions
            if q.get("source", "").lower() == persona.lower()
            or q.get("persona", "").lower() == persona.lower()
        ]

    total = len(questions)
    by_class = Counter(q.get("ddc_class", q.get("score", "unknown")) for q in questions)

    gaps = [
        q for q in questions
        if q.get("ddc_class", q.get("score", "")) in ("INCOMPLETE", "MISSING", "partial", "not_answerable")
    ]

    return {
        "block": block_name,
        "total_questions": total,
        "coverage": dict(by_class),
        "gap_count": len(gaps),
        "persona_filter": persona,
        "gaps": [
            {
                "question": g.get("question", ""),
                "ddc_class": g.get("ddc_class", g.get("score", "")),
                "source": g.get("source", g.get("persona", "")),
                "gaps_detected": g.get("gaps", []),
            }
            for g in gaps[:20]
        ],
    }


def run_server(output_dir: str = ""):
    """Entry point for the CLI command."""
    global _single_output, _project_root
    if output_dir:
        _single_output = output_dir
        os.environ["CB_OUTPUT_DIR"] = output_dir
    else:
        from context_blocks.blocks import find_project_root
        _project_root = find_project_root()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    mcp.run(transport="stdio")
