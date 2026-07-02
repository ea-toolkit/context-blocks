"""Post-extraction entity dedup — merge ambiguous entities.

Scans entity files, groups candidates by name similarity,
LLM judges each pair (merge vs keep), merges the files.

Usage:
    context-blocks dedup --output <dir>
"""
import json
import os
import re
from pathlib import Path

import structlog
import yaml

logger = structlog.get_logger(__name__)


def find_candidates(entity_dir: Path, threshold: float = 0.5) -> list[tuple[dict, dict]]:
    """Find entity pairs that might be duplicates based on name similarity.

    Returns list of (entity_a, entity_b) tuples where each entity is a dict
    with: id, name, type, description, filepath, confidence.
    """
    entities = []
    for type_dir in sorted(entity_dir.iterdir()):
        if not type_dir.is_dir():
            continue
        for filepath in sorted(type_dir.glob("*.md")):
            entity = _parse_entity_meta(filepath)
            if entity:
                entities.append(entity)

    logger.info("dedup_scan", total_entities=len(entities))

    # Group candidates by name similarity (Jaccard on words)
    candidates = []
    stop_words = {"the", "a", "an", "and", "or", "for", "of", "to", "in", "is", "on", "at", "by"}

    for i, a in enumerate(entities):
        a_words = set(re.findall(r"\w+", a["name"].lower())) - stop_words
        for b in entities[i + 1:]:
            # Skip if different entity types (system vs process = different things)
            # But allow same type or closely related types
            if a["type"] != b["type"]:
                continue

            b_words = set(re.findall(r"\w+", b["name"].lower())) - stop_words
            if not a_words or not b_words:
                continue

            jaccard = len(a_words & b_words) / len(a_words | b_words)
            if jaccard >= threshold:
                candidates.append((a, b))

    # Also check for prefix/suffix patterns: "X" vs "X Deployment", "X" vs "X v2"
    name_map: dict[str, list[dict]] = {}
    for e in entities:
        base = re.sub(r"\s+(deployment|v\d+|process|processing|monitoring|migration)$", "", e["name"].lower()).strip()
        name_map.setdefault(base, []).append(e)

    for base, group in name_map.items():
        if len(group) > 1:
            for i, a in enumerate(group):
                for b in group[i + 1:]:
                    pair = (a, b)
                    # Avoid duplicate pairs
                    if pair not in candidates and (b, a) not in candidates:
                        candidates.append(pair)

    logger.info("dedup_candidates", pairs=len(candidates))
    return candidates


def judge_pair(
    a: dict, b: dict,
    api_key: str | None = None,
    model: str | None = None,
    provider: str | None = None,
) -> dict:
    """Ask LLM whether two entities should be merged.

    Uses litellm for provider-agnostic LLM calls. Respects LLM_PROVIDER
    and LLM_MODEL environment variables.

    Returns: {"action": "merge"|"keep", "reason": str, "keep_id": str}
    """
    import litellm

    provider = provider or os.environ.get("LLM_PROVIDER", "anthropic")
    model = model or os.environ.get("LLM_MODEL", "claude-sonnet-4-6")
    api_key = api_key or os.environ.get("LLM_API_KEY", "")

    if provider == "openai":
        litellm_model = model
    else:
        litellm_model = f"{provider}/{model}"

    prompt = f"""You are reviewing two entities from a domain knowledge base to determine if they are duplicates that should be merged.

Entity A:
  ID: {a['id']}
  Name: {a['name']}
  Type: {a['type']}
  Description: {a['description']}
  Confidence: {a['confidence']}

Entity B:
  ID: {b['id']}
  Name: {b['name']}
  Type: {b['type']}
  Description: {b['description']}
  Confidence: {b['confidence']}

Decide:
- MERGE if these refer to the same concept (e.g., "Claims Gateway" and "Claims Gateway Deployment" are aspects of the same system)
- KEEP if these are genuinely different concepts (e.g., "Claims Submission API v1" and "Claims Submission API v2" are different versions)

Return JSON: {{"action": "merge"|"keep", "reason": "brief explanation", "keep_id": "id of the more complete entity if merging"}}
Return ONLY the JSON, no other text."""

    try:
        response = litellm.completion(
            model=litellm_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            api_key=api_key,
        )
    except Exception as e:
        logger.error("dedup_judge_api_error", a=a["name"], b=b["name"], error=str(e))
        return {"action": "keep", "reason": f"API error: {e}", "keep_id": a["id"]}

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("dedup_judge_parse_failed", text=text[:100])
        result = {"action": "keep", "reason": "parse error", "keep_id": a["id"]}

    usage = response.usage
    logger.info(
        "dedup_judged",
        a=a["name"],
        b=b["name"],
        action=result.get("action"),
        reason=result.get("reason", "")[:60],
        input_tokens=getattr(usage, "prompt_tokens", 0),
        output_tokens=getattr(usage, "completion_tokens", 0),
    )

    return result


def merge_entities(keep: dict, remove: dict, entity_dir: Path) -> None:
    """Merge two entity files — keep the more complete one, append unique info from the other."""
    keep_path = Path(keep["filepath"])
    remove_path = Path(remove["filepath"])

    if not keep_path.exists() or not remove_path.exists():
        logger.warning("dedup_merge_skip", reason="file not found")
        return

    keep_content = keep_path.read_text(encoding="utf-8")
    remove_content = remove_path.read_text(encoding="utf-8")

    # Parse both YAML frontmatters
    keep_parts = keep_content.split("---", 2)
    remove_parts = remove_content.split("---", 2)

    if len(keep_parts) < 3 or len(remove_parts) < 3:
        logger.warning("dedup_merge_skip", reason="bad frontmatter")
        return

    keep_fm = yaml.safe_load(keep_parts[1])
    remove_fm = yaml.safe_load(remove_parts[1])

    # Merge relationships — union of both
    standard_fields = {"type", "id", "name", "description", "status", "tags",
                       "source_documents", "confidence"}
    for key, value in remove_fm.items():
        if key not in standard_fields and key not in keep_fm:
            keep_fm[key] = value
        elif key not in standard_fields and key in keep_fm:
            # Merge list values
            if isinstance(keep_fm[key], list) and isinstance(value, list):
                existing = set(str(v) for v in keep_fm[key])
                for v in value:
                    if str(v) not in existing:
                        keep_fm[key].append(v)

    # Merge source_documents
    keep_sources = set(keep_fm.get("source_documents", []) or [])
    remove_sources = set(remove_fm.get("source_documents", []) or [])
    keep_fm["source_documents"] = sorted(keep_sources | remove_sources)

    # Keep higher confidence
    keep_fm["confidence"] = max(
        keep_fm.get("confidence", 0.5),
        remove_fm.get("confidence", 0.5),
    )

    # Merge body — append unique content from removed entity
    keep_body = keep_parts[2].strip()
    remove_body = remove_parts[2].strip()

    if remove_body and remove_body not in keep_body:
        # Add a section noting the merge
        keep_body += f"\n\n## Additional Details (merged from {remove['name']})\n\n{remove_body}"

    # Write updated keep file
    new_content = f"---\n{yaml.dump(keep_fm, default_flow_style=False, sort_keys=False)}---\n\n{keep_body}\n"
    keep_path.write_text(new_content, encoding="utf-8")

    # Delete the removed file
    remove_path.unlink()

    logger.info("dedup_merged", kept=keep["name"], removed=remove["name"])


def run_dedup(
    entity_dir: Path,
    api_key: str | None = None,
    dry_run: bool = False,
) -> list[dict]:
    """Run the full dedup pipeline. Returns merge log."""
    candidates = find_candidates(entity_dir)

    if not candidates:
        logger.info("dedup_no_candidates")
        return []

    merge_log = []

    for a, b in candidates:
        judgment = judge_pair(a, b, api_key=api_key)

        log_entry = {
            "entity_a": a["name"],
            "entity_a_id": a["id"],
            "entity_b": b["name"],
            "entity_b_id": b["id"],
            "action": judgment["action"],
            "reason": judgment.get("reason", ""),
            "keep_id": judgment.get("keep_id", ""),
        }
        merge_log.append(log_entry)

        if judgment["action"] == "merge" and not dry_run:
            keep_id = judgment.get("keep_id", a["id"])
            if keep_id == b["id"]:
                merge_entities(keep=b, remove=a, entity_dir=entity_dir)
            else:
                merge_entities(keep=a, remove=b, entity_dir=entity_dir)

    return merge_log


def _parse_entity_meta(filepath: Path) -> dict | None:
    """Extract metadata from an entity markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        fm = yaml.safe_load(parts[1].strip())
        if not fm or not isinstance(fm, dict):
            return None

        return {
            "id": fm.get("id", filepath.stem),
            "name": fm.get("name", filepath.stem),
            "type": fm.get("type", filepath.parent.name),
            "description": fm.get("description", ""),
            "confidence": fm.get("confidence", 0.5) if isinstance(fm.get("confidence"), (int, float)) else 0.5,
            "filepath": str(filepath),
        }
    except Exception as e:
        logger.warning("entity_parse_failed", filepath=str(filepath), error=str(e))
        return None
