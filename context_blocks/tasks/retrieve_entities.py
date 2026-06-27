"""Retrieve Entities task — finds previously extracted entities relevant to the current document.

Simple keyword matching for v1. Can be upgraded to embedding-based retrieval later.
The agent gets specific entity details for things mentioned in the current document,
without carrying ALL entities in every prompt.
"""

from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)


def get_all_entity_ids(output_dir: Path) -> list[dict[str, str]]:
    """Get ALL existing entity IDs grouped by type — used to prevent duplicate ID creation.

    Returns a tree structure so the agent can distinguish:
    - order-processor (system) vs order-processor-db (software-component)

    Args:
        output_dir: Directory containing entity files.

    Returns:
        List of dicts with 'id', 'type', 'name' for each entity.
    """
    entities_dir = output_dir / "entities"
    if not entities_dir.exists():
        return []

    entities = []
    for entity_file in entities_dir.rglob("*.md"):
        # Type comes from parent directory name
        entity_type = entity_file.parent.name
        entity_id = entity_file.stem

        # Try to read the name from frontmatter
        name = entity_id  # fallback
        try:
            for line in entity_file.read_text(encoding="utf-8").split("\n"):
                if line.strip().startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                    break
        except Exception:
            pass

        entities.append({
            "id": entity_id,
            "type": entity_type,
            "name": name,
        })

    return sorted(entities, key=lambda e: (e["type"], e["id"]))


def retrieve_relevant_entities(
    document_content: str,
    output_dir: Path,
    max_entities: int = 10,
) -> str:
    """Find previously extracted entities that are relevant to the current document.

    Uses simple keyword matching: if an entity's name or ID appears in the document,
    include it. Keeps prompt focused on what's relevant.

    Args:
        document_content: The text of the document about to be analyzed.
        output_dir: Directory containing previously extracted entity files.
        max_entities: Maximum number of entities to include.

    Returns:
        Formatted string of relevant entity summaries for the prompt.
    """
    entities_dir = output_dir / "entities"
    if not entities_dir.exists():
        return ""

    # Collect all entity files
    entity_files = list(entities_dir.rglob("*.md"))
    if not entity_files:
        return ""

    # Score each entity by relevance to the document
    doc_lower = document_content.lower()
    scored_entities = []

    for entity_file in entity_files:
        try:
            content = entity_file.read_text(encoding="utf-8")

            # Extract name and ID from frontmatter
            name, entity_id, entity_type, description = _parse_entity_header(content)

            if not name:
                continue

            # Score: how many times does the entity name/ID appear in the document?
            score = 0
            name_lower = name.lower()
            id_lower = entity_id.lower() if entity_id else ""

            # Check name presence (whole word matching would be better, but simple for v1)
            if name_lower in doc_lower:
                score += 3
            # Check ID presence
            if id_lower and id_lower in doc_lower:
                score += 2
            # Check individual significant words from the name (3+ chars)
            for word in name_lower.split():
                if len(word) >= 4 and word in doc_lower:
                    score += 1

            if score > 0:
                scored_entities.append({
                    "name": name,
                    "id": entity_id,
                    "type": entity_type,
                    "description": description,
                    "score": score,
                })

        except Exception as e:
            logger.debug("entity_retrieval_skip", file=entity_file.name, error=str(e))
            continue

    # Sort by score, take top N
    scored_entities.sort(key=lambda x: x["score"], reverse=True)
    top_entities = scored_entities[:max_entities]

    if not top_entities:
        return ""

    # Format for prompt
    lines = [
        f"### Previously Extracted Entities Relevant to This Document ({len(top_entities)})",
        "",
        "These entities were extracted from earlier documents. If this document adds new information about them, UPDATE your understanding — don't create duplicates.",
        "",
    ]

    for entity in top_entities:
        lines.append(f"- **{entity['name']}** ({entity['type']}): {entity['description']}")

    logger.info(
        "entities_retrieved",
        relevant_count=len(top_entities),
        total_available=len(entity_files),
        retrieved_ids=[e["id"] for e in top_entities],
        scores={e["id"]: e["score"] for e in top_entities},
    )

    return "\n".join(lines)


def _parse_entity_header(content: str) -> tuple[str, str, str, str]:
    """Extract name, ID, type, and description from entity file frontmatter.

    Returns:
        Tuple of (name, id, type, description). Empty strings if not found.
    """
    name = ""
    entity_id = ""
    entity_type = ""
    description = ""

    in_frontmatter = False

    for line in content.split("\n"):
        line = line.strip()
        if line == "---":
            if in_frontmatter:
                break  # End of frontmatter
            in_frontmatter = True
            continue

        if in_frontmatter:
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            elif line.startswith("id:"):
                entity_id = line.split(":", 1)[1].strip()
            elif line.startswith("type:"):
                entity_type = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip()

    return name, entity_id, entity_type, description
