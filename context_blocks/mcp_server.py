"""Context Blocks MCP Server — expose KB to AI agents via Model Context Protocol.

Knowledge tools (read-only) — query what a block knows:
- list_blocks: discover available context blocks (domains)
- get_overview: KB stats and structure for a block
- search_entities: find entities by text query
- get_entity: full detail for one entity
- ask_kb: DAR retrieval pipeline (with LLM synthesis if API key set, retrieval-only otherwise)
- get_gap_report: coverage gaps, optionally per persona
- list_artifacts: list a block's non-md files (diagrams, images, xml)
- fetch_file: read a file inside a block by relative path (artifact or entity)

Routing tool — where to fetch live data / act (pointers, never credentials):
- resolve_source: routing map for a live-system entity (logs, incidents, dashboards, APIs)

Work-effort tools — the demand log (group an agent's calls under one intent):
- begin_work_effort / end_work_effort: open/close one unit of work
- get_work_efforts: read back what agents asked and where the block fell short

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

from context_blocks import temporal, tracing

mcp = FastMCP(
    "Context Blocks",
    instructions="Query domain knowledge bases built by Context Blocks. "
    "Start with list_blocks() to see available domains, then use the block name "
    "in other tools. If there's only one block, it's used automatically.",
)

_block_cache: dict[str, dict] = {}
_project_root: Path = Path.cwd()
_single_output: str = ""

# Current work-effort (one intent, grouping this agent's call-chain). Set by
# begin_work_effort, cleared by end_work_effort. Read tools auto-log to it when
# set. Safe for stdio MCP (one agent per process); note the caveat for a shared
# HTTP server (state would be process-global across agents).
_current_we: str = ""
_current_we_dir: str = ""


def _trace(tool: str, args: dict, summary: str, is_gap: bool) -> None:
    """Log one read-tool call to the active work-effort, if any. No-op otherwise."""
    if not _current_we or not _current_we_dir:
        return
    try:
        tracing.log_call(_current_we_dir, _current_we, tool, args, summary, is_gap)
    except Exception:
        # Tracing must never break a query.
        pass

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


def _layer_for_type(etype: str) -> str:
    from context_blocks.ontology import get_active_ontology

    ont = get_active_ontology()
    if ont is not None:
        layer = ont.get_layer(etype)
        if layer and layer != "unknown":
            return layer.title()
    return LAYER_MAP.get(etype, "Other")


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
            try:
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
                    "layer": _layer_for_type(etype),
                    "description": fm.get("description", ""),
                    "status": fm.get("status", "active"),
                    "confidence": fm.get("confidence", 1.0),
                    "relationships": _extract_rels(fm),
                    "source_documents": fm.get("source_documents", []),
                    "routing": fm.get("routing") if isinstance(fm.get("routing"), dict) else {},
                    "body": body.strip(),
                    "file": str(filepath),
                })
            except Exception:
                continue
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


def _apply_block_ontology(block: str) -> None:
    """Set the active ontology to the block's custom ontology (drives type→layer mapping)."""
    from context_blocks.ontology import load_ontology_from_file, set_active_ontology

    try:
        from context_blocks.blocks import BlockRegistry, find_project_root

        cfg = BlockRegistry(find_project_root()).resolve_block(block)
        onto = getattr(cfg, "ontology", "default") or "default"
        if onto != "default" and Path(onto).exists():
            set_active_ontology(load_ontology_from_file(onto))
            return
    except Exception:
        pass
    set_active_ontology(None)


def _resolve_block(block: str) -> dict:
    """Resolve a block name to its cached data. Loads entities on first access."""
    available = _get_available_blocks()

    if not available:
        return {"error": "No blocks found. Run cb init or cb extract first."}

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
            _apply_block_ontology(block)
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
        return [{"message": "No blocks found. Run cb init or cb extract first."}]

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
def list_artifacts(block: str = "") -> list[dict]:
    """List the non-markdown artifacts attached to a block — diagrams (.bpmn/.drawio/.uml), images, and xml files. These are NOT searchable knowledge (use search_entities/ask_kb for that); they are supporting files an entity references, e.g. an architecture diagram. Returns each artifact's filename, path (relative to the block), size in bytes, and content_type. Use fetch_file(path) to read a text artifact; binary images should be fetched via the HTTP artifact endpoint. Pass block name from list_blocks(); if only one block exists it's used automatically."""
    data = _resolve_block(block)
    if "error" in data:
        return [data]
    from context_blocks import storage

    arts = storage.list_artifacts(Path(data["output_dir"]))
    return [
        {"filename": a.filename, "path": a.path, "size": a.size, "content_type": a.content_type}
        for a in arts
    ]


@mcp.tool()
def fetch_file(path: str, block: str = "") -> dict:
    """Fetch the raw content of a file inside a block by its path relative to the block — e.g. 'artifacts/order-flow.bpmn', 'entities/systems/payment-gateway.md', or 'seed-context.md'. Use this to read a diagram/xml artifact (from list_artifacts) or an entity file in full. Returns {path, content_type, content} for text files. Binary files (images) are not returned as text — you get {path, content_type, size, note} instead; fetch those via the HTTP artifact endpoint. Pass block name from list_blocks(); if only one block exists it's used automatically."""
    data = _resolve_block(block)
    if "error" in data:
        return data
    output_dir = Path(data["output_dir"]).resolve()
    target = (output_dir / path).resolve()
    if not target.is_relative_to(output_dir):
        return {"error": f"Path escapes the block: {path}"}
    if not target.is_file():
        return {"error": f"File not found: {path}"}

    from context_blocks import storage

    content_type = storage.guess_content_type(target.name)
    try:
        return {"path": path, "content_type": content_type, "content": target.read_text(encoding="utf-8")}
    except UnicodeDecodeError:
        return {
            "path": path,
            "content_type": content_type,
            "size": target.stat().st_size,
            "note": "Binary file — not returned as text. Fetch via the HTTP artifact endpoint.",
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

    results = [
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
    _trace(
        "search_entities",
        {"query": query, "entity_type": entity_type, "layer": layer},
        f"{len(results)} hits: {[r['id'] for r in results][:8]}",
        is_gap=(len(results) == 0),
    )
    return results


@mcp.tool()
def get_entity(entity_id: str, block: str = "") -> dict:
    """Get the complete detail for one entity. Use after search_entities() returns an id you want to explore, or when you already know the entity id (kebab-case, e.g. 'claims-gateway', 'claim-routing-process'). Pass block name from list_blocks() or omit for single-block projects. Returns: id, name, type, layer, status, confidence score (0-1), description, full markdown body, all relationships (type + target_id), and source documents that created this entity. Returns {error: '...'} if the id doesn't exist."""
    data = _resolve_block(block)
    if "error" in data:
        return data

    index = data.get("entity_index", {})
    e = index.get(entity_id)
    if not e:
        _trace("get_entity", {"entity_id": entity_id}, "not found", is_gap=True)
        return {"error": f"Entity '{entity_id}' not found in block '{data['name']}'"}

    _trace("get_entity", {"entity_id": entity_id}, f"got {entity_id}", is_gap=False)
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
def resolve_source(entity_id: str = "", query: str = "", block: str = "") -> dict:
    """Resolve the ROUTING for live systems — where to go to fetch fresh data or take action (logs, incidents, dashboards, APIs). This is the map to the live source, NOT the knowledge itself, and NOT credentials (those live in your own workspace, never here). Pass an entity_id (e.g. 'grafana-loki', 'nowit', 'wom-connector') for that system's routing, or a query to find systems whose routing matches (e.g. 'logs', 'incidents'). Returns {block, sources: [{id, name, type, routing}]} where routing is a dict of read-only pointers. Typical flow: search_entities/get_entity tells you which system is involved → resolve_source tells you where its data lives → then use your workspace tools + credentials to actually call it."""
    data = _resolve_block(block)
    if "error" in data:
        return data

    def _has_routing(e: dict) -> bool:
        r = e.get("routing")
        return isinstance(r, dict) and len(r) > 0

    if entity_id:
        e = data.get("entity_index", {}).get(entity_id)
        if not e:
            _trace("resolve_source", {"entity_id": entity_id}, "entity not found", is_gap=True)
            return {"error": f"Entity '{entity_id}' not found in block '{data['name']}'"}
        if not _has_routing(e):
            _trace("resolve_source", {"entity_id": entity_id}, "no routing curated", is_gap=True)
            return {"block": data["name"], "sources": [],
                    "note": f"'{entity_id}' has no routing — it may not be a live system, or its routing isn't curated yet."}
        _trace("resolve_source", {"entity_id": entity_id}, f"routed to {entity_id}", is_gap=False)
        return {"block": data["name"],
                "sources": [{"id": e["id"], "name": e["name"], "type": e["type"], "routing": e["routing"]}]}

    terms = set(re.findall(r"\w+", query.lower())) if query else set()
    sources = []
    for e in data.get("entities", []):
        if not _has_routing(e):
            continue
        if terms:
            hay = set(re.findall(r"\w+", f"{e['name']} {e['description']} {e['routing']}".lower()))
            if not (terms & hay):
                continue
        sources.append({"id": e["id"], "name": e["name"], "type": e["type"], "routing": e["routing"]})
    _trace("resolve_source", {"query": query}, f"{len(sources)} sources: {[s['id'] for s in sources][:8]}",
           is_gap=(len(sources) == 0))
    return {"block": data["name"], "sources": sources}


@mcp.tool()
def begin_work_effort(intent: str, block: str = "", agent: str = "") -> dict:
    """Open a WORK-EFFORT — one unit of work with one intent (e.g. 'triage INC12345: WOM connector timeouts'). Call this FIRST when you start working a problem, before you search/get/resolve. Every KB call you make until end_work_effort is grouped under this one intent, forming the demand log: what you needed, what you found, and where the KB fell short. Returns {work_effort_id, block, intent}. This is how the block learns what to curate next — always open one before real work, and close it with end_work_effort when done."""
    global _current_we, _current_we_dir
    data = _resolve_block(block)
    if "error" in data:
        return data
    wid = tracing.begin(data["output_dir"], data["name"], intent, agent)
    _current_we = wid
    _current_we_dir = data["output_dir"]
    return {"work_effort_id": wid, "block": data["name"], "intent": intent}


@mcp.tool()
def end_work_effort(outcome: str = "") -> dict:
    """Close the active work-effort with an OUTCOME — a one-line result of the unit of work (e.g. 'resolved: purged stuck Solace queue', 'escalated to blue-team', 'no runbook found — gap'). Call this when you finish the problem you opened with begin_work_effort. Returns {closed, outcome}. The outcome plus the call-chain is the demand signal: recurring intents and gap-heavy efforts are exactly what the block should curate next."""
    global _current_we, _current_we_dir
    if not _current_we:
        return {"note": "No active work-effort to close."}
    wid = _current_we
    tracing.end(_current_we_dir, wid, outcome)
    _current_we = ""
    _current_we_dir = ""
    return {"closed": wid, "outcome": outcome}


@mcp.tool()
def get_work_efforts(block: str = "", limit: int = 20) -> dict:
    """Read the DEMAND LOG — recent work-efforts on a block, each with its full call-chain (search → get → resolve → outcome) and which calls hit gaps. Use this to see what agents actually ask a block, where the knowledge falls short (gap-heavy efforts), and what recurring intents deserve curation. Returns {block, work_efforts: [{intent, outcome, call_count, gap_count, calls:[...]}]}. This is the curation backlog, written by real use — not guessed."""
    data = _resolve_block(block)
    if "error" in data:
        return data
    return {"block": data["name"],
            "work_efforts": tracing.get_work_efforts(data["output_dir"], limit)}


@mcp.tool()
def get_events(block: str = "", entity_id: str = "", limit: int = 50) -> dict:
    """Read the CHANGE HISTORY of a block — the temporal event log (created/updated events, newest first), each with a timestamp and the actor who made it. Pass entity_id to see one entity's history, or omit for the whole block. Returns {block, events: [{at, entity_id, entity_type, action, actor, work_effort_id, summary}]}. Use this to answer 'when did this knowledge change and who touched it', or to power a freshness/churn view. Everything the block persists is timestamped and attributed."""
    data = _resolve_block(block)
    if "error" in data:
        return data
    return {"block": data["name"],
            "events": temporal.get_events(data["output_dir"], limit=limit,
                                          entity_id=entity_id or None)}


@mcp.tool()
async def ask_kb(question: str, block: str = "") -> dict:
    """Retrieve domain knowledge for a question. Runs the DAR pipeline: intent classification, parallel search (vector + keyword + graph), RRF fusion, and gap detection. No server-side LLM call is made — the calling agent should synthesize the final answer from the returned context_text and entities. Use for questions like 'How does claim routing work?', 'What systems depend on the claims gateway?'. Pass block name from list_blocks(). First call per block is slow (~5s) as it loads embeddings; subsequent calls are fast. Returns: mode ('synthesis' or 'retrieval'), entities (ranked by relevance with scores, types, layers), context_text (assembled domain context — use this to synthesize your answer), intent (query classification weights), gaps (knowledge gaps with severity and suggested actions), and total_ms. If LLM_API_KEY is set server-side, additionally returns: answer (pre-synthesized), ddc_class (CLEAN/INCOMPLETE/MISSING), citations."""
    data = _resolve_block(block)
    if "error" in data:
        return data

    output_dir = data["output_dir"]
    entity_dir = output_dir / "entities"
    block_name = data["name"]

    if not entity_dir.exists():
        return {"error": f"No entities found in block '{block_name}'. Run cb extract first."}

    llm_key = os.environ.get("LLM_API_KEY", "")
    has_llm = bool(llm_key)
    cache_key = f"pipeline_{block_name}_{'synth' if has_llm else 'retrieval'}"

    from context_blocks.retrieval.backend import InMemoryBackend
    from context_blocks.retrieval.embedder import get_embedder, index_entities
    from context_blocks.retrieval.pipeline import RetrievalPipeline

    if cache_key not in _block_cache:
        try:
            backend = InMemoryBackend()
            backend.load_from_entity_dir(entity_dir)

            openai_key = os.environ.get("OPENAI_API_KEY")
            emb = get_embedder(provider="auto", api_key=openai_key)
            await index_entities(backend, emb)

            synth_fn = None
            if has_llm:
                from context_blocks.retrieval.synthesis import get_synthesizer
                synth_fn = get_synthesizer(provider="anthropic", api_key=llm_key)

            pipeline = RetrievalPipeline(backend, embed_fn=emb.embed, synthesize_fn=synth_fn)
            _block_cache[cache_key] = {"pipeline": pipeline}
        except Exception as e:
            return {"error": f"Failed to initialize pipeline for block '{block_name}': {e}"}

    pipeline = _block_cache[cache_key]["pipeline"]

    try:
        result = await pipeline.retrieve(question)
    except Exception as e:
        return {"error": f"Retrieval failed: {e}", "block": block_name}

    ddc_map = {"answerable": "CLEAN", "partial": "INCOMPLETE", "not_answerable": "MISSING"}
    hops = result.trace.hops

    response = {
        "block": block_name,
        "question": question,
        "mode": "synthesis" if has_llm else "retrieval",
        "entities": [
            {
                "id": h.entity_id,
                "name": h.entity_name,
                "type": h.entity_type,
                "layer": h.layer,
                "confidence": h.confidence,
                "score": h.fused_score,
                "found_by": h.found_by or [h.matched_by],
            }
            for h in hops
        ],
        "context_text": result.context_text,
        "intent": result.trace.intent_weights,
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

    if has_llm:
        response["answer"] = result.answer
        response["ddc_class"] = ddc_map.get(result.score.value, "MISSING")
        response["citations"] = result.citations

    return response


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


def run_server(
    output_dir: str = "",
    transport: str = "",
    host: str = "",
    port: int = 0,
):
    """Entry point for the CLI command."""
    global _single_output, _project_root
    if output_dir:
        _single_output = output_dir
        os.environ["CB_OUTPUT_DIR"] = output_dir
    else:
        from context_blocks.blocks import find_project_root
        _project_root = find_project_root()

    resolved_transport = transport or os.environ.get("CB_MCP_TRANSPORT", "stdio")
    resolved_host = host or os.environ.get("CB_MCP_HOST", "127.0.0.1")
    resolved_port = port or int(os.environ.get("CB_MCP_PORT", "8000"))

    if resolved_transport in ("streamable-http", "sse"):
        mcp.settings.host = resolved_host
        mcp.settings.port = resolved_port

    mcp.run(transport=resolved_transport)


if __name__ == "__main__":
    mcp.run(transport="stdio")
