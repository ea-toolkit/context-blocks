"""End-to-end: a custom (non-default) ontology must be honored across ALL subsystems.

This is the regression test that was missing — every subsystem used to assume the default
18-type meta-model, so custom ontologies silently fell back to it. This exercises the full
non-LLM path (prompt, validation, directory routing, file write, export layer mapping) with a
custom ontology active, and asserts each subsystem uses the custom types/layers.
"""

import textwrap
from pathlib import Path

import pytest
from pydantic import ValidationError

from context_blocks.export_obsidian import _layer_for_type as obsidian_layer
from context_blocks.export_skill import _layer_for_type as skill_layer
from context_blocks.mcp_server import _layer_for_type as mcp_layer
from context_blocks.meta_model import format_meta_model_for_prompt, get_directory_for_type
from context_blocks.models.entity import ExtractedEntity
from context_blocks.ontology import load_ontology_from_file, set_active_ontology
from context_blocks.tasks.write_entities import write_entity_file


def _custom_ontology_yaml() -> str:
    return textwrap.dedent("""\
        layers:
          structural: { label: Structural, question: "What exists?", color: "#000" }
          behavioral: { label: Behavioral, question: "How?", color: "#000" }
        entity_types:
          incident: { layer: behavioral, directory: incidents, label: Incidents }
          service:  { layer: structural, directory: services, label: Services }
        relationship_fields:
          - affects
          - resolved_by
    """)


@pytest.fixture()
def custom_ontology(tmp_path: Path):
    (tmp_path / "meta-model.yaml").write_text(_custom_ontology_yaml())
    ont = load_ontology_from_file(tmp_path / "meta-model.yaml")
    set_active_ontology(ont)
    yield ont
    set_active_ontology(None)


def _entity(entity_type: str) -> ExtractedEntity:
    return ExtractedEntity(
        entity_type=entity_type, id="wom-service", name="Work Order Service",
        description="d", overview="o", details="dd", confidence=0.9,
    )


class TestCustomOntologyHonoredEverywhere:
    def test_prompt_renders_custom_types_not_default(self, custom_ontology) -> None:
        out = format_meta_model_for_prompt()
        assert "incident" in out and "service" in out
        assert "**system**" not in out  # default types are gone

    def test_validation_accepts_custom_rejects_others(self, custom_ontology) -> None:
        assert _entity("incident").entity_type == "incident"
        with pytest.raises(ValidationError):
            _entity("system")   # default type, not in custom ontology
        with pytest.raises(ValidationError):
            _entity("banana")   # unknown

    def test_directory_routing_uses_custom_dir(self, custom_ontology) -> None:
        assert get_directory_for_type("incident") == "incidents"
        assert get_directory_for_type("service") == "services"

    def test_file_write_lands_in_custom_dir_with_custom_type(self, custom_ontology, tmp_path: Path) -> None:
        out = tmp_path / "block"
        path = write_entity_file(_entity("incident"), out, "some-doc.md")
        # Written under the custom directory...
        assert path == out / "entities" / "incidents" / "wom-service.md"
        assert path.exists()
        # ...with the custom type in frontmatter (not coerced to a default)
        assert "type: incident" in path.read_text()

    def test_export_layer_mapping_uses_custom_layers(self, custom_ontology) -> None:
        # All three export/MCP layer resolvers must honor the active ontology
        for resolver in (skill_layer, obsidian_layer, mcp_layer):
            assert resolver("incident") == "Behavioral"
            assert resolver("service") == "Structural"


class TestDefaultUnchangedWithoutCustomOntology:
    """No active ontology → identical default behavior (opt-in safety)."""

    def test_default_prompt_and_routing(self) -> None:
        set_active_ontology(None)
        out = format_meta_model_for_prompt()
        assert "system" in out
        assert get_directory_for_type("system") == "systems"
        assert _entity("system").entity_type == "system"
        # Export layer resolvers fall back to the default map
        assert skill_layer("system") == "Structural"
