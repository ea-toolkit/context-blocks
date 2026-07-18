"""Ontology loader — reads meta-model YAML to determine entity types, layers, and relationship fields.

Search order for meta-model.yaml:
  1. Block's entity directory parent (e.g., .context-blocks/cortex/meta-model.yaml)
  2. Project root (meta-model.yaml next to blocks.yaml)
  3. viewer/src/config/meta-model.yaml (CB development)
  4. Built-in defaults (matches CB's 56 relationship types and 18 entity types)

An "active ontology" contextvar is set during extraction (see set_active_ontology). Prompt
builders, entity-type validation, directory routing, and retry hints all read it, so a block's
custom ontology drives extraction without threading it through every function. None → built-in
defaults (unchanged behavior).
"""

from __future__ import annotations

import contextvars
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

# Canonical layer order for grouping types in the prompt.
_LAYER_ORDER = ["structural", "behavioral", "reference", "organizational", "language", "decision"]


@dataclass
class Ontology:
    """Loaded ontology config — types, layers, directories, and relationship allowlist."""

    relationship_fields: set[str] = field(default_factory=lambda: set(DEFAULT_RELATIONSHIP_FIELDS))
    type_to_layer: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_TYPE_TO_LAYER))
    type_to_directory: dict[str, str] = field(default_factory=dict)
    type_to_label: dict[str, str] = field(default_factory=dict)
    source: str = "defaults"

    def is_relationship_field(self, field_name: str) -> bool:
        return field_name in self.relationship_fields

    def get_layer(self, entity_type: str) -> str:
        return self.type_to_layer.get(entity_type, "unknown")

    @property
    def types(self) -> set[str]:
        """The set of entity type names this ontology defines."""
        return set(self.type_to_layer.keys())

    def is_known_type(self, entity_type: str) -> bool:
        return entity_type in self.type_to_layer

    def directory_for(self, entity_type: str) -> str | None:
        return self.type_to_directory.get(entity_type)

    def format_for_prompt(self) -> str:
        """Render types (grouped by layer) + relationship fields for the extraction prompt."""
        by_layer: dict[str, list[str]] = {}
        for t, layer in self.type_to_layer.items():
            by_layer.setdefault(layer, []).append(t)

        lines = [f"## Entity Meta-Model ({len(self.type_to_layer)} Types)\n"]
        seen: set[str] = set()
        for layer in _LAYER_ORDER + sorted(by_layer.keys()):
            if layer in seen or layer not in by_layer:
                continue
            seen.add(layer)
            lines.append(f"\n### {layer.title()} Layer")
            for t in sorted(by_layer[layer]):
                label = self.type_to_label.get(t, "")
                lines.append(f"- **{t}**{f' — {label}' if label else ''}")

        lines.append("\n\n## Available Relationship Fields")
        lines.append("Use these to connect entities (generic `depends_on`, `related_to`, `part_of` are always available):")
        lines.append(", ".join(f"`{r}`" for r in sorted(self.relationship_fields)))
        return "\n".join(lines)


# ── Active-ontology context (set during extraction; read by prompts/validation/routing) ──

_active_ontology: contextvars.ContextVar[Ontology | None] = contextvars.ContextVar(
    "cb_active_ontology", default=None
)


def set_active_ontology(ont: Ontology | None) -> None:
    """Set the ontology in effect for the current extraction. None → built-in defaults."""
    _active_ontology.set(ont)


def get_active_ontology() -> Ontology | None:
    """The ontology in effect for the current extraction, or None (use built-in defaults)."""
    return _active_ontology.get()


def load_ontology(entity_dir: Path | None = None) -> Ontology:
    """Load ontology from meta-model.yaml, searching from entity_dir upward."""
    search_paths: list[Path] = []

    if entity_dir:
        search_paths.append(entity_dir.parent / "meta-model.yaml")
        search_paths.append(entity_dir.parent.parent / "meta-model.yaml")

    search_paths.append(Path("viewer/src/config/meta-model.yaml"))

    for config_path in search_paths:
        if config_path.exists():
            try:
                return _parse_config(config_path)
            except Exception as e:
                logger.warning("ontology_parse_failed", path=str(config_path), error=str(e))

    logger.info("ontology_using_defaults")
    return Ontology()


def load_ontology_from_file(config_path: Path | str) -> Ontology:
    """Load an ontology from an explicit meta-model.yaml path (e.g. a block's registered ontology)."""
    return _parse_config(Path(config_path))


def _parse_config(config_path: Path) -> Ontology:
    """Parse a meta-model.yaml into an Ontology."""
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Expected dict, got {type(raw).__name__}")

    rel_fields = set()
    if "relationship_fields" in raw:
        rel_fields = {str(f) for f in raw["relationship_fields"] if isinstance(f, str)}

    type_to_layer: dict[str, str] = {}
    type_to_directory: dict[str, str] = {}
    type_to_label: dict[str, str] = {}
    if "entity_types" in raw:
        for type_key, type_config in raw["entity_types"].items():
            if isinstance(type_config, dict):
                if "layer" in type_config:
                    type_to_layer[type_key] = type_config["layer"]
                if "directory" in type_config:
                    type_to_directory[type_key] = type_config["directory"]
                if "label" in type_config:
                    type_to_label[type_key] = type_config["label"]

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
        type_to_directory=type_to_directory,
        type_to_label=type_to_label,
        source=str(config_path),
    )
