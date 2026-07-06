"""Ontology loader — reads meta-model YAML to determine entity types, layers, and relationship fields.

Search order for meta-model.yaml:
  1. Block's entity directory parent (e.g., .context-blocks/cortex/meta-model.yaml)
  2. Project root (meta-model.yaml next to blocks.yaml)
  3. viewer/src/config/meta-model.yaml (CB development)
  4. Built-in defaults (matches CB's 56 relationship types and 18 entity types)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import structlog
import yaml

logger = structlog.get_logger(__name__)

DEFAULT_RELATIONSHIP_FIELDS: set[str] = {
    "related_to", "depends_on", "supersedes", "part_of",
    "owned_by", "governed_by", "made_by",
    "deployed_on", "belongs_to", "hosts", "hosted_by", "used_by", "enables", "requires",
    "exposes", "exposed_by", "consumed_by", "contracts",
    "persists", "sourced_from", "contains", "maps_to", "produced_by", "parameterises",
    "triggers", "triggered_by", "produces", "consumes", "published_by", "carries",
    "handles", "communicates_with",
    "executed_by", "involves", "initiates", "serves", "served_by",
    "implements", "realised_by", "powered_by", "provided_by", "integrated_via", "provides",
    "enforced_by", "applies_to", "derives_from", "documented_in", "enforced_via", "motivated_by",
    "supports", "uses", "enabled_by",
    "used_in", "defined_by", "synonymous_with", "contrasts_with",
}

DEFAULT_TYPE_TO_LAYER: dict[str, str] = {
    "system": "structural", "software-component": "structural",
    "api": "structural", "data-model": "structural",
    "data-product": "structural", "platform": "structural",
    "process": "behavioral", "business-event": "behavioral",
    "domain-logic": "behavioral", "reference-data": "reference",
    "team": "organizational", "persona": "organizational",
    "capability": "organizational", "offering": "organizational",
    "external-party": "organizational",
    "jargon-business": "language", "jargon-tech": "language",
    "decision": "decision",
}


@dataclass
class Ontology:
    """Loaded ontology config — relationship allowlist and type-to-layer mapping."""

    relationship_fields: set[str] = field(default_factory=lambda: set(DEFAULT_RELATIONSHIP_FIELDS))
    type_to_layer: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_TYPE_TO_LAYER))
    source: str = "defaults"

    def is_relationship_field(self, field_name: str) -> bool:
        return field_name in self.relationship_fields

    def get_layer(self, entity_type: str) -> str:
        return self.type_to_layer.get(entity_type, "unknown")


def load_ontology(entity_dir: Path | None = None) -> Ontology:
    """Load ontology from meta-model.yaml, searching from entity_dir upward."""
    search_paths: list[Path] = []

    if entity_dir:
        # Block-level: .context-blocks/cortex/meta-model.yaml (entity_dir is .../cortex/entities)
        search_paths.append(entity_dir.parent / "meta-model.yaml")
        # Project-level: next to blocks.yaml
        search_paths.append(entity_dir.parent.parent / "meta-model.yaml")

    # Viewer config (CB development)
    search_paths.append(Path("viewer/src/config/meta-model.yaml"))

    for config_path in search_paths:
        if config_path.exists():
            try:
                return _parse_config(config_path)
            except Exception as e:
                logger.warning("ontology_parse_failed", path=str(config_path), error=str(e))

    logger.info("ontology_using_defaults")
    return Ontology()


def _parse_config(config_path: Path) -> Ontology:
    """Parse a meta-model.yaml into an Ontology."""
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Expected dict, got {type(raw).__name__}")

    # Relationship fields — allowlist
    rel_fields = set()
    if "relationship_fields" in raw:
        rel_fields = {str(f) for f in raw["relationship_fields"] if isinstance(f, str)}

    # Type-to-layer mapping
    type_to_layer = {}
    if "entity_types" in raw:
        for type_key, type_config in raw["entity_types"].items():
            if isinstance(type_config, dict) and "layer" in type_config:
                type_to_layer[type_key] = type_config["layer"]

    # Fall back to defaults if YAML is present but sections are missing
    if not rel_fields:
        rel_fields = set(DEFAULT_RELATIONSHIP_FIELDS)
    if not type_to_layer:
        type_to_layer = dict(DEFAULT_TYPE_TO_LAYER)

    logger.info(
        "ontology_loaded",
        source=str(config_path),
        relationship_fields=len(rel_fields),
        entity_types=len(type_to_layer),
    )

    return Ontology(
        relationship_fields=rel_fields,
        type_to_layer=type_to_layer,
        source=str(config_path),
    )
