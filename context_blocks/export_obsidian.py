"""Export KB entities as an Obsidian-compatible vault with wikilinks."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


def export_obsidian(entity_dir: Path, output_dir: Path) -> dict[str, int]:
    """Export entities to an Obsidian vault.

    Returns dict with counts: entities, relationships_linked, types.
    """
    if not entity_dir.exists():
        msg = f"Entity directory not found: {entity_dir}"
        raise FileNotFoundError(msg)

    output_dir.mkdir(parents=True, exist_ok=True)

    # First pass: build ID → display name map for wikilinks
    id_to_name: dict[str, str] = {}
    id_to_type: dict[str, str] = {}
    entity_files: list[tuple[Path, dict, str]] = []

    for md_file in entity_dir.rglob("*.md"):
        raw = md_file.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(raw)
        if not fm:
            continue
        eid = fm.get("id", md_file.stem)
        name = fm.get("name", eid)
        etype = fm.get("type", md_file.parent.name)
        id_to_name[eid] = name
        id_to_type[eid] = etype
        entity_files.append((md_file, fm, body))

    # Relationship fields to convert to wikilinks
    rel_fields = [
        "related_to", "depends_on", "owned_by", "deployed_on",
        "implements_capability", "consumes", "produces", "triggers",
        "triggered_by", "affects", "affected_by", "source_documents",
        "related_systems", "related_processes", "triggered",
        "published_by", "subscribed_by", "managed_by",
    ]

    stats = {"entities": 0, "relationships_linked": 0, "types": set()}
    moc_entries: dict[str, list[str]] = {}

    # Second pass: write entities with wikilinks
    for md_file, fm, body in entity_files:
        etype = fm.get("type", md_file.parent.name)
        eid = fm.get("id", md_file.stem)
        name = fm.get("name", eid)

        # Build obsidian frontmatter (subset of original)
        obs_fm = {
            "type": etype,
            "id": eid,
            "name": name,
            "aliases": [eid, name],
        }
        if fm.get("description"):
            obs_fm["description"] = fm["description"]
        if fm.get("status"):
            obs_fm["status"] = fm["status"]
        if fm.get("confidence"):
            obs_fm["confidence"] = fm["confidence"]
        if fm.get("tags"):
            obs_fm["tags"] = fm["tags"]

        # Convert relationship fields to wikilink sections
        rel_sections = []
        link_count = 0
        for field in rel_fields:
            refs = fm.get(field)
            if not refs:
                continue
            if isinstance(refs, str):
                refs = [refs]
            links = []
            for ref in refs:
                display = id_to_name.get(ref, ref)
                links.append(f"[[{display}]]")
                link_count += 1
            rel_sections.append(f"**{_humanize(field)}:** {', '.join(links)}")

        stats["relationships_linked"] += link_count

        # Strip duplicate H1 if it matches the entity name
        body_stripped = _strip_leading_h1(body, name)

        # Convert inline entity references in body to wikilinks
        linked_body = _linkify_body(body_stripped, id_to_name)

        # Assemble the file
        type_dir = output_dir / _type_dirname(etype)
        type_dir.mkdir(parents=True, exist_ok=True)

        parts = [
            "---",
            yaml.dump(obs_fm, default_flow_style=False, sort_keys=False).strip(),
            "---",
            "",
            f"# {name}",
            "",
        ]

        if rel_sections:
            parts.append("## Relationships")
            parts.append("")
            parts.extend(rel_sections)
            parts.append("")

        if linked_body.strip():
            parts.append(linked_body.strip())
            parts.append("")

        out_file = type_dir / f"{eid}.md"
        out_file.write_text("\n".join(parts), encoding="utf-8")

        stats["entities"] += 1
        stats["types"].add(etype)

        # Track for MOC
        layer = _layer_for_type(etype)
        moc_entries.setdefault(layer, []).append(f"- [[{name}]] ({etype})")

    # Write Map of Content
    _write_moc(output_dir, moc_entries, stats)

    return {
        "entities": stats["entities"],
        "relationships_linked": stats["relationships_linked"],
        "types": len(stats["types"]),
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


def _strip_leading_h1(body: str, name: str) -> str:
    """Remove the first H1 if it matches the entity name (avoids duplicate heading)."""
    lines = body.lstrip("\n").split("\n", 1)
    if lines and lines[0].strip().lstrip("# ").strip() == name:
        return lines[1] if len(lines) > 1 else ""
    return body


def _humanize(field: str) -> str:
    return field.replace("_", " ").title()


def _type_dirname(etype: str) -> str:
    return etype.replace("_", "-")


def _linkify_body(body: str, id_to_name: dict[str, str]) -> str:
    """Replace entity name references in body text with wikilinks.

    Only matches whole words, skips headers and existing links.
    Only links names >= 4 chars to avoid false positives.
    """
    lines = body.split("\n")
    linked = set()
    result = []

    for line in lines:
        if line.startswith("#") or "[[" in line:
            result.append(line)
            continue

        for _eid, name in sorted(id_to_name.items(), key=lambda x: -len(x[1])):
            if name in linked or len(name) < 4:
                continue
            pattern = re.compile(r"\b" + re.escape(name) + r"\b")
            if pattern.search(line):
                line = pattern.sub(f"[[{name}]]", line, count=1)
                linked.add(name)

        result.append(line)

    return "\n".join(result)


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


def _write_moc(output_dir: Path, entries: dict[str, list[str]], stats: dict) -> None:
    lines = [
        "# Knowledge Base — Map of Content",
        "",
        f"> {stats['entities']} entities across {len(stats['types'])} types",
        "",
    ]

    layer_order = ["Structural", "Behavioral", "Reference", "Organizational", "Language", "Decision", "Other"]
    for layer in layer_order:
        items = entries.get(layer, [])
        if not items:
            continue
        lines.append(f"## {layer}")
        lines.append("")
        lines.extend(sorted(items))
        lines.append("")

    (output_dir / "MOC.md").write_text("\n".join(lines), encoding="utf-8")
