"""Context Blocks Viewer — the storybook of your domain.

Run: python -m context_blocks.viewer --output .private/output
Opens a browser showing the domain knowledge base as a navigable story.
"""

import json
import re
from pathlib import Path

import typer
import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app_cli = typer.Typer()
app_api = FastAPI(title="Context Blocks")

_output_dir: Path = Path("output")

# Layer definitions matching the meta-model
LAYERS = {
    "structural": {
        "label": "Structural",
        "question": "What exists?",
        "color": "#4A90E2",
        "dirs": ["systems", "software-components", "apis", "data-models", "data-products", "platforms"],
    },
    "behavioral": {
        "label": "Behavioral",
        "question": "How does it work?",
        "color": "#1ABC9C",
        "dirs": ["processes", "business-events", "domain-logic"],
    },
    "reference": {
        "label": "Reference",
        "question": "What are the allowed values?",
        "color": "#0891B2",
        "dirs": ["reference-data"],
    },
    "organizational": {
        "label": "Organizational",
        "question": "Who is involved?",
        "color": "#9B59B6",
        "dirs": ["teams", "personas", "capabilities", "offerings", "external-parties"],
    },
    "language": {
        "label": "Language",
        "question": "What do terms mean?",
        "color": "#F39C12",
        "dirs": ["jargon-business", "jargon-tech"],
    },
    "decision": {
        "label": "Decision",
        "question": "Why was this chosen?",
        "color": "#B45309",
        "dirs": ["decisions"],
    },
}

TYPE_LABELS = {
    "systems": "Systems",
    "software-components": "Software Components",
    "apis": "APIs",
    "data-models": "Data Models",
    "data-products": "Data Products",
    "platforms": "Platforms",
    "processes": "Processes",
    "business-events": "Business Events",
    "domain-logic": "Domain Logic",
    "reference-data": "Reference Data",
    "teams": "Teams",
    "personas": "Personas",
    "capabilities": "Capabilities",
    "offerings": "Offerings",
    "external-parties": "External Parties",
    "jargon-business": "Business Jargon",
    "jargon-tech": "Technical Jargon",
    "decisions": "Decisions",
}


def _load_entities(output_dir: Path) -> list[dict]:
    """Load all entity files from the output directory."""
    entities_dir = output_dir / "entities"
    if not entities_dir.exists():
        return []

    entities = []
    for entity_file in sorted(entities_dir.rglob("*.md")):
        try:
            content = entity_file.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            if len(parts) < 3:
                continue

            fm = yaml.safe_load(parts[1].strip()) or {}
            body = parts[2].strip()

            # Extract open questions from body
            open_questions = []
            if "## Open Questions" in body:
                q_section = body.split("## Open Questions")[1].split("##")[0]
                open_questions = [
                    line.strip().lstrip("- ")
                    for line in q_section.strip().split("\n")
                    if line.strip().startswith("- ")
                ]

            # Determine layer
            entity_type_dir = entity_file.parent.name
            layer = "structural"
            for layer_key, layer_info in LAYERS.items():
                if entity_type_dir in layer_info["dirs"]:
                    layer = layer_key
                    break

            entities.append({
                **fm,
                "body": body,
                "open_questions": open_questions,
                "entity_type_dir": entity_type_dir,
                "type_label": TYPE_LABELS.get(entity_type_dir, entity_type_dir),
                "layer": layer,
                "file": str(entity_file.relative_to(output_dir)),
            })
        except Exception:
            continue

    return entities


def _load_domain_summary(output_dir: Path) -> dict:
    """Load the domain understanding from the analysis report."""
    report_path = output_dir / "analysis-report.md"
    if not report_path.exists():
        return {"summary": "", "relationships": "", "questions": []}

    content = report_path.read_text(encoding="utf-8")

    # Extract domain understanding
    summary = ""
    if "## Current Domain Understanding" in content:
        section = content.split("## Current Domain Understanding")[1]
        section = section.split("---")[0]
        # Get main prose (before ### subsections)
        parts = section.split("###")
        summary = parts[0].strip()

    # Extract key relationships
    relationships = ""
    if "### Key Relationships" in content:
        rel_section = content.split("### Key Relationships")[1]
        rel_section = rel_section.split("###")[0].split("---")[0]
        relationships = rel_section.strip()

    # Extract open questions from report
    report_questions = []
    if "### Open Questions" in content:
        q_section = content.split("### Open Questions")[1]
        q_section = q_section.split("##")[0].split("---")[0]
        report_questions = [
            line.strip().lstrip("- ")
            for line in q_section.strip().split("\n")
            if line.strip().startswith("- ")
        ]

    return {
        "summary": summary,
        "relationships": relationships,
        "questions": report_questions,
    }


def _build_graph_data(entities: list[dict]) -> dict:
    """Build nodes and edges for the domain context map."""
    nodes = []
    edges = []
    entity_ids = {e.get("id") for e in entities}

    # All possible relationship fields
    rel_fields = [
        "related_to", "depends_on", "owned_by", "implements", "produces",
        "consumes", "triggers", "part_of", "deployed_on", "belongs_to",
        "hosts", "hosted_by", "used_by", "enables", "exposes", "exposed_by",
        "consumed_by", "contracts", "persists", "sourced_from", "contains",
        "maps_to", "produced_by", "parameterises", "triggered_by", "published_by",
        "carries", "handles", "communicates_with", "executed_by", "involves",
        "initiates", "serves", "served_by", "realised_by", "powered_by",
        "provided_by", "integrated_via", "provides", "enforced_by", "applies_to",
        "derives_from", "documented_in", "enforced_via", "motivated_by",
        "used_in", "defined_by", "synonymous_with", "contrasts_with",
        "made_by", "governed_by", "responsible_for", "owns",
    ]

    for entity in entities:
        eid = entity.get("id", "")
        layer = entity.get("layer", "structural")
        layer_info = LAYERS.get(layer, LAYERS["structural"])
        conf = entity.get("confidence", 0)

        nodes.append({
            "id": eid,
            "label": entity.get("name", eid),
            "type": entity.get("type", ""),
            "layer": layer,
            "color": layer_info["color"],
            "confidence": conf,
        })

        for rel_type in rel_fields:
            targets = entity.get(rel_type, [])
            if isinstance(targets, str):
                targets = [targets]
            if targets:
                for target in targets:
                    if target and target in entity_ids:
                        edges.append({
                            "source": eid,
                            "target": target,
                            "type": rel_type,
                        })

    return {"nodes": nodes, "edges": edges}


@app_api.get("/", response_class=HTMLResponse)
async def index():
    return _render_storybook("story")


@app_api.get("/map", response_class=HTMLResponse)
async def domain_map():
    return _render_storybook("map")


@app_api.get("/entities", response_class=HTMLResponse)
async def entities_page():
    return _render_storybook("entities")


@app_api.get("/entities/{entity_id}", response_class=HTMLResponse)
async def entity_detail(entity_id: str):
    return _render_storybook("entity", entity_id=entity_id)


@app_api.get("/questions", response_class=HTMLResponse)
async def questions_page():
    return _render_storybook("questions")


@app_api.get("/glossary", response_class=HTMLResponse)
async def glossary_page():
    return _render_storybook("glossary")


@app_api.get("/api/entities")
async def api_entities():
    return _load_entities(_output_dir)


@app_api.get("/api/graph")
async def api_graph():
    entities = _load_entities(_output_dir)
    return _build_graph_data(entities)


def _render_storybook(page: str, entity_id: str | None = None) -> HTMLResponse:
    """Render the storybook viewer."""
    entities = _load_entities(_output_dir)
    domain = _load_domain_summary(_output_dir)
    graph = _build_graph_data(entities)

    # Compute stats
    total = len(entities)
    all_questions = []
    for e in entities:
        for q in e.get("open_questions", []):
            all_questions.append({"question": q, "entity_id": e.get("id"), "entity_name": e.get("name")})
    all_questions.extend([{"question": q, "entity_id": None, "entity_name": "Domain-level"} for q in domain.get("questions", [])])

    sources = set()
    for e in entities:
        for s in e.get("source_documents", []):
            sources.add(s)

    high_conf = sum(1 for e in entities if e.get("confidence", 0) >= 0.85)
    low_conf = sum(1 for e in entities if e.get("confidence", 0) < 0.7)

    # Group by layer, then by type
    by_layer = {}
    for layer_key, layer_info in LAYERS.items():
        layer_entities = [e for e in entities if e.get("layer") == layer_key]
        if layer_entities:
            by_type = {}
            for e in layer_entities:
                t = e.get("entity_type_dir", "unknown")
                by_type.setdefault(t, []).append(e)
            by_layer[layer_key] = {
                "info": layer_info,
                "by_type": by_type,
                "count": len(layer_entities),
            }

    # Jargon for glossary
    jargon = [e for e in entities if e.get("layer") == "language"]
    jargon.sort(key=lambda e: e.get("name", "").lower())

    template_path = Path(__file__).parent / "viewer_template.html"
    template = template_path.read_text(encoding="utf-8")

    # Build JSON data
    entities_map = {e.get("id"): e for e in entities}
    stats_data = {
        "total": total,
        "questions": len(all_questions),
        "sources": len(sources),
        "high_conf": high_conf,
        "low_conf": low_conf,
        "layers": {k: v["count"] for k, v in by_layer.items()},
        "edges": len(graph["edges"]),
    }
    by_layer_data = {
        k: {
            "label": v["info"]["label"],
            "question": v["info"]["question"],
            "color": v["info"]["color"],
            "count": v["count"],
            "types": {t: [e.get("id") for e in ents] for t, ents in v["by_type"].items()},
        } for k, v in by_layer.items()
    }
    jargon_data = [{"id": e.get("id"), "name": e.get("name"), "type": e.get("entity_type_dir"), "description": e.get("description", "")} for e in jargon]

    # Inject data into template
    js_data = (
        f"const PAGE = {json.dumps(page)};\n"
        f"const ENTITY_ID = {json.dumps(entity_id)};\n"
        f"const ENTITIES = {json.dumps(entities_map)};\n"
        f"const GRAPH = {json.dumps(graph)};\n"
        f"const DOMAIN = {json.dumps(domain)};\n"
        f"const STATS = {json.dumps(stats_data)};\n"
        f"const ALL_QUESTIONS = {json.dumps(all_questions)};\n"
        f"const BY_LAYER = {json.dumps(by_layer_data)};\n"
        f"const LAYERS_CONFIG = {json.dumps(LAYERS)};\n"
        f"const TYPE_LABELS = {json.dumps(TYPE_LABELS)};\n"
        f"const JARGON = {json.dumps(jargon_data)};\n"
    )
    html = template.replace("/*DATA_INJECT*/", js_data)

    return HTMLResponse(html)


@app_cli.command()
def serve(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities"),
    port: int = typer.Option(8090, "--port", "-p", help="Port to serve on"),
    open_browser: bool = typer.Option(True, "--open/--no-open", help="Open browser automatically"),
) -> None:
    """Launch the Context Blocks viewer in your browser."""
    global _output_dir
    _output_dir = output

    entities = _load_entities(output)
    questions = sum(len(e.get("open_questions", [])) for e in entities)

    print(f"\n  Context Blocks — Domain Storybook\n")
    print(f"  Entities:   {len(entities)}")
    print(f"  Questions:  {questions}")
    print(f"  Output:     {output}")
    print(f"  URL:        http://localhost:{port}\n")

    if open_browser:
        import threading
        import webbrowser
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    uvicorn.run(app_api, host="0.0.0.0", port=port, log_level="warning")


if __name__ == "__main__":
    app_cli()
