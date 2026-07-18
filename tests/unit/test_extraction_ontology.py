"""Tests for #79 — extraction honoring a block's custom ontology (prompt, validation, routing)."""

import textwrap
from pathlib import Path

import pytest
from pydantic import ValidationError

from context_blocks.meta_model import format_meta_model_for_prompt, get_directory_for_type
from context_blocks.models.entity import ExtractedEntity
from context_blocks.ontology import (
    Ontology,
    get_active_ontology,
    load_ontology_from_file,
    set_active_ontology,
)


@pytest.fixture(autouse=True)
def _reset_active_ontology():
    """Keep the active-ontology contextvar from leaking between tests."""
    set_active_ontology(None)
    yield
    set_active_ontology(None)


def _incident_ontology() -> Ontology:
    return Ontology(
        relationship_fields={"affects", "resolved_by"},
        type_to_layer={"incident": "behavioral", "runbook": "behavioral", "service": "structural"},
        type_to_directory={"incident": "incidents", "runbook": "runbooks", "service": "services"},
        type_to_label={"incident": "Incidents"},
        source="test-incident",
    )


def _entity(entity_type: str) -> dict:
    return dict(
        entity_type=entity_type, id="x", name="X", description="d",
        overview="o", details="dd", confidence=0.9,
    )


class TestPromptRendering:
    def test_default_prompt_has_default_types(self) -> None:
        out = format_meta_model_for_prompt()
        assert "system" in out
        assert "incident" not in out  # default meta-model has no 'incident' type

    def test_custom_ontology_prompt_has_custom_types(self) -> None:
        set_active_ontology(_incident_ontology())
        out = format_meta_model_for_prompt()
        assert "incident" in out and "runbook" in out
        assert "**system**" not in out  # default types are gone

    def test_explicit_ontology_arg_overrides_context(self) -> None:
        out = format_meta_model_for_prompt(_incident_ontology())
        assert "incident" in out


class TestDirectoryRouting:
    def test_default_directory(self) -> None:
        assert get_directory_for_type("system") == "systems"

    def test_custom_directory(self) -> None:
        set_active_ontology(_incident_ontology())
        assert get_directory_for_type("incident") == "incidents"
        assert get_directory_for_type("runbook") == "runbooks"

    def test_unmapped_custom_type_falls_back_to_name(self) -> None:
        set_active_ontology(Ontology(type_to_layer={"widget": "structural"}, source="t"))
        assert get_directory_for_type("widget") == "widget"


class TestEntityTypeValidation:
    def test_default_valid_type_ok(self) -> None:
        assert ExtractedEntity(**_entity("system")).entity_type == "system"

    def test_default_invalid_type_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ExtractedEntity(**_entity("banana"))

    def test_custom_type_accepted_when_ontology_active(self) -> None:
        set_active_ontology(_incident_ontology())
        assert ExtractedEntity(**_entity("incident")).entity_type == "incident"

    def test_default_type_rejected_under_custom_ontology(self) -> None:
        # 'system' is a default type but NOT in the incident ontology → rejected
        set_active_ontology(_incident_ontology())
        with pytest.raises(ValidationError):
            ExtractedEntity(**_entity("system"))

    def test_unknown_type_rejected_under_custom_ontology(self) -> None:
        set_active_ontology(_incident_ontology())
        with pytest.raises(ValidationError):
            ExtractedEntity(**_entity("banana"))


class TestOntologyLoader:
    def test_load_from_file_parses_directory_and_label(self, tmp_path: Path) -> None:
        yaml_content = textwrap.dedent("""\
            entity_types:
              incident:
                layer: behavioral
                directory: incidents
                label: Incidents
              service:
                layer: structural
                directory: services
            relationship_fields:
              - affects
        """)
        f = tmp_path / "meta-model.yaml"
        f.write_text(yaml_content)

        ont = load_ontology_from_file(f)
        assert ont.is_known_type("incident")
        assert ont.directory_for("incident") == "incidents"
        assert ont.type_to_label["incident"] == "Incidents"
        assert ont.types == {"incident", "service"}
        assert "affects" in ont.relationship_fields

    def test_set_get_active_ontology(self) -> None:
        assert get_active_ontology() is None
        ont = _incident_ontology()
        set_active_ontology(ont)
        assert get_active_ontology() is ont
