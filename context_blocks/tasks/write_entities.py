"""Write Entities task — outputs entity markdown files with YAML frontmatter.

Takes extraction results and writes one file per entity,
organized by type into subdirectories. Also saves raw extraction
JSON for re-rendering without re-calling the LLM.
"""

import json
from pathlib import Path

import structlog
import yaml

from context_blocks.meta_model import get_directory_for_type
from context_blocks.models.entity import DocumentExtractionResult, ExtractedEntity

logger = structlog.get_logger(__name__)


def save_extraction_json(result: DocumentExtractionResult, output_dir: Path) -> Path:
    """Save the raw extraction result as JSON for later re-rendering.

    This is the expensive artifact — the LLM output. Markdown entity files
    are a cheap render that can be regenerated from this JSON at any time.

    Args:
        result: The extraction result from analyzing a document.
        output_dir: Root output directory.

    Returns:
        Path to the saved JSON file.
    """
    extractions_dir = output_dir / "extractions"
    extractions_dir.mkdir(parents=True, exist_ok=True)

    # Use full source document filename (with extension replaced) to avoid
    # collisions when .txt and .md share the same base name
    safe_name = result.source_document.replace(".", "-").replace("/", "-")
    filepath = extractions_dir / f"{safe_name}.json"

    filepath.write_text(
        result.model_dump_json(indent=2),
        encoding="utf-8",
    )

    logger.debug(
        "extraction_json_saved",
        source_document=result.source_document,
        filepath=str(filepath),
        entities=len(result.entities),
    )

    return filepath


def load_extraction_json(filepath: Path) -> DocumentExtractionResult:
    """Load a saved extraction result from JSON.

    Args:
        filepath: Path to the JSON file.

    Returns:
        The deserialized extraction result.
    """
    data = json.loads(filepath.read_text(encoding="utf-8"))
    return DocumentExtractionResult.model_validate(data)


def load_all_extractions(output_dir: Path) -> list[DocumentExtractionResult]:
    """Load all saved extraction results from the extractions directory.

    Args:
        output_dir: Root output directory.

    Returns:
        List of extraction results, sorted by source document name.
    """
    extractions_dir = output_dir / "extractions"
    if not extractions_dir.exists():
        return []

    results = []
    for filepath in sorted(extractions_dir.glob("*.json")):
        try:
            result = load_extraction_json(filepath)
            results.append(result)
        except Exception as e:
            logger.warning(
                "extraction_json_load_failed",
                filepath=str(filepath),
                error=str(e),
            )

    return results


def reformat_all_entities(output_dir: Path) -> int:
    """Regenerate all entity markdown files from saved extraction JSON.

    Clears the entities/ directory and rewrites everything from the
    raw extraction JSON. This is a free operation — no API calls.

    Args:
        output_dir: Root output directory containing extractions/.

    Returns:
        Total number of entity files written.
    """
    results = load_all_extractions(output_dir)
    if not results:
        logger.warning("reformat_no_extractions", output_dir=str(output_dir))
        return 0

    # Clear existing entities directory
    entities_dir = output_dir / "entities"
    if entities_dir.exists():
        import shutil
        shutil.rmtree(entities_dir)
        logger.info("reformat_cleared_entities", path=str(entities_dir))

    # Rewrite all entities from saved JSON
    total = 0
    for result in results:
        written = write_extraction_results(result, output_dir)
        total += len(written)

    logger.info(
        "reformat_complete",
        documents=len(results),
        entities=total,
    )

    return total


def write_entity_file(entity: ExtractedEntity, output_dir: Path, source_document: str) -> Path:
    """Write a single entity as a markdown file with YAML frontmatter.

    Args:
        entity: The extracted entity to write.
        output_dir: Root output directory (e.g., ./output).
        source_document: The document this entity was extracted from.

    Returns:
        Path to the written file.
    """
    # Determine directory based on entity type
    type_dir = get_directory_for_type(entity.entity_type)
    entity_dir = output_dir / "entities" / type_dir
    entity_dir.mkdir(parents=True, exist_ok=True)

    # Build YAML frontmatter
    frontmatter = {
        "type": entity.entity_type,
        "id": entity.id,
        "name": entity.name,
        "description": entity.description,
        "status": entity.status,
        "tags": entity.tags if entity.tags else [],
        "source_documents": [source_document],
        "confidence": entity.confidence,
    }

    # Add relationships if present (deduplicated)
    if entity.relationships:
        for rel in entity.relationships:
            rel_key = rel.relationship_type
            if rel_key not in frontmatter:
                frontmatter[rel_key] = []
            if isinstance(frontmatter[rel_key], list):
                if rel.target_entity_id not in frontmatter[rel_key]:
                    frontmatter[rel_key].append(rel.target_entity_id)
            else:
                if frontmatter[rel_key] != rel.target_entity_id:
                    frontmatter[rel_key] = [frontmatter[rel_key], rel.target_entity_id]

    # Build markdown body
    body_lines = [
        f"# {entity.name}",
        "",
        "## Overview",
        "",
        entity.overview,
        "",
        "## Details",
        "",
        entity.details,
    ]

    # Add hedged statements as open questions section
    if entity.hedged_statements:
        body_lines.append("")
        body_lines.append("## Open Questions")
        body_lines.append("")
        for hs in entity.hedged_statements:
            body_lines.append(f"- {hs}")

    filepath = entity_dir / f"{entity.id}.md"

    if filepath.exists():
        # Entity already exists — MERGE, never overwrite
        content = _merge_entity(filepath, entity, source_document, frontmatter, body_lines)
    else:
        content = _format_entity_file(frontmatter, "\n".join(body_lines))

    filepath.write_text(content, encoding="utf-8")

    logger.debug(
        "entity_written",
        entity_id=entity.id,
        entity_type=entity.entity_type,
        filepath=str(filepath),
    )

    return filepath


def write_extraction_results(
    result: DocumentExtractionResult,
    output_dir: Path,
) -> list[Path]:
    """Write all entities from an extraction result to files.

    Args:
        result: The extraction result from analyzing a document.
        output_dir: Root output directory.

    Returns:
        List of paths to written entity files.
    """
    written_files = []

    for entity in result.entities:
        filepath = write_entity_file(entity, output_dir, result.source_document)
        written_files.append(filepath)

    logger.info(
        "entities_written",
        source_document=result.source_document,
        count=len(written_files),
        output_dir=str(output_dir),
    )

    return written_files


def _merge_entity(
    existing_path: Path,
    new_entity: ExtractedEntity,
    source_document: str,
    new_frontmatter: dict,
    new_body_lines: list[str],
) -> str:
    """Merge new extraction into an existing entity file.

    Rules:
    - Never delete existing content
    - Append new information with source citation
    - Mark conflicts when new info contradicts existing
    - Union relationships and source_documents
    """
    existing_content = existing_path.read_text(encoding="utf-8")

    # Parse existing frontmatter and body
    existing_fm, existing_body = _parse_existing_entity(existing_content)

    # Merge source_documents (union)
    existing_sources = existing_fm.get("source_documents", [])
    if source_document not in existing_sources:
        existing_sources.append(source_document)
    new_frontmatter["source_documents"] = existing_sources

    # Identify relationship keys (anything in existing frontmatter that's not a standard field)
    standard_fields = {"type", "id", "name", "description", "status", "tags", "source_documents", "confidence"}
    existing_rel_keys = {k for k in existing_fm if k not in standard_fields}

    # Build set of existing relationship pairs for dedup
    existing_rels: set[str] = set()
    for key in existing_rel_keys:
        vals = existing_fm[key]
        if isinstance(vals, list):
            for v in vals:
                existing_rels.add(f"{key}:{v}")
        else:
            existing_rels.add(f"{key}:{vals}")

    # Clear relationship keys from new_frontmatter (they were added during initial
    # frontmatter build in write_entity_file — we rebuild them here with proper dedup)
    for key in list(new_frontmatter.keys()):
        if key not in standard_fields:
            del new_frontmatter[key]

    # Collect ALL relationship targets: existing file + new entity, deduplicated
    merged_rels: dict[str, list[str]] = {}

    # Add existing relationships
    for key in existing_rel_keys:
        vals = existing_fm[key]
        if isinstance(vals, list):
            merged_rels[key] = list(dict.fromkeys(vals))
        else:
            merged_rels[key] = [vals]

    # Add new entity relationships (dedup against existing)
    for rel in new_entity.relationships:
        rel_key = rel.relationship_type
        if rel_key not in merged_rels:
            merged_rels[rel_key] = []
        if rel.target_entity_id not in merged_rels[rel_key]:
            merged_rels[rel_key].append(rel.target_entity_id)

    # Write merged relationships to frontmatter
    for key, vals in merged_rels.items():
        new_frontmatter[key] = vals if len(vals) > 1 else vals[0]

    # Confidence = max of existing and new
    existing_confidence = existing_fm.get("confidence", 0)
    new_frontmatter["confidence"] = max(existing_confidence, new_entity.confidence)

    # Build merged body — existing content + new additions
    new_section = f"\n\n## Additional Details\n[from {source_document}]\n\n"
    new_section += new_entity.details

    # Check for potential conflicts in description
    conflicts = []
    existing_desc = existing_fm.get("description", "")
    if existing_desc and new_entity.description and existing_desc != new_entity.description:
        # Don't replace description, but note if significantly different
        if len(set(existing_desc.lower().split()) & set(new_entity.description.lower().split())) < 3:
            conflicts.append(
                f"Description differs: existing says '{existing_desc}', "
                f"[{source_document}] says '{new_entity.description}'"
            )
    # Keep existing description
    new_frontmatter["description"] = existing_desc or new_entity.description

    # Build final body
    merged_body = existing_body.rstrip()
    merged_body += new_section

    if conflicts:
        merged_body += "\n\n## Conflicts\n"
        for conflict in conflicts:
            merged_body += f"\n⚠️ {conflict}\n"

    logger.info(
        "entity_merged",
        entity_id=new_entity.id,
        new_source=source_document,
        total_sources=len(existing_sources),
        conflicts=len(conflicts),
    )

    return _format_entity_file(new_frontmatter, merged_body)


def _parse_existing_entity(content: str) -> tuple[dict, str]:
    """Parse an existing entity file into frontmatter dict and body string."""
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_str = parts[1].strip()
    body = parts[2].strip()

    # Parse YAML frontmatter
    fm = {}
    try:
        fm = yaml.safe_load(frontmatter_str) or {}
    except Exception:
        pass

    return fm, body


def _format_entity_file(frontmatter: dict, body: str) -> str:
    """Format a complete entity file with YAML frontmatter + markdown body."""

    # Use block scalar style for long description strings
    class BlockStr(str):
        pass

    def block_str_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
        if "\n" in data or len(data) > 80:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    dumper = yaml.Dumper
    dumper.add_representer(str, block_str_representer)

    yaml_str = yaml.dump(
        frontmatter,
        Dumper=dumper,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )
    return f"---\n{yaml_str}---\n\n{body}\n"
