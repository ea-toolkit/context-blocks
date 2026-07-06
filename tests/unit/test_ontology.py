"""Tests for ontology loading and relationship field allowlisting."""

import textwrap
from pathlib import Path

import pytest

from context_blocks.ontology import (
    DEFAULT_RELATIONSHIP_FIELDS,
    DEFAULT_TYPE_TO_LAYER,
    Ontology,
    load_ontology,
)


class TestOntologyDefaults:
    def test_default_relationship_fields(self) -> None:
        ont = Ontology()
        assert ont.relationship_fields == DEFAULT_RELATIONSHIP_FIELDS
        assert "related_to" in ont.relationship_fields
        assert "depends_on" in ont.relationship_fields

    def test_default_type_to_layer(self) -> None:
        ont = Ontology()
        assert ont.get_layer("system") == "structural"
        assert ont.get_layer("process") == "behavioral"
        assert ont.get_layer("team") == "organizational"
        assert ont.get_layer("jargon-business") == "language"
        assert ont.get_layer("decision") == "decision"

    def test_unknown_type_returns_unknown(self) -> None:
        ont = Ontology()
        assert ont.get_layer("journey") == "unknown"
        assert ont.get_layer("nonexistent") == "unknown"

    def test_is_relationship_field(self) -> None:
        ont = Ontology()
        assert ont.is_relationship_field("related_to") is True
        assert ont.is_relationship_field("depends_on") is True
        assert ont.is_relationship_field("make_or_buy") is False
        assert ont.is_relationship_field("source") is False
        assert ont.is_relationship_field("method") is False


class TestOntologyFromYaml:
    def test_loads_from_block_dir(self, tmp_path: Path) -> None:
        block_dir = tmp_path / "my-block"
        entity_dir = block_dir / "entities"
        entity_dir.mkdir(parents=True)

        yaml_content = textwrap.dedent("""\
            entity_types:
              system:
                layer: structural
              journey:
                layer: behavioral

            relationship_fields:
              - related_to
              - parent_capability
              - owns_systems
        """)
        (block_dir / "meta-model.yaml").write_text(yaml_content)

        ont = load_ontology(entity_dir)
        assert ont.source == str(block_dir / "meta-model.yaml")
        assert ont.get_layer("system") == "structural"
        assert ont.get_layer("journey") == "behavioral"
        assert ont.is_relationship_field("parent_capability") is True
        assert ont.is_relationship_field("make_or_buy") is False
        assert len(ont.relationship_fields) == 3

    def test_falls_back_to_defaults_when_no_yaml(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        entity_dir = tmp_path / "block" / "entities"
        entity_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        ont = load_ontology(entity_dir)
        assert ont.source == "defaults"
        assert ont.relationship_fields == DEFAULT_RELATIONSHIP_FIELDS
        assert ont.type_to_layer == DEFAULT_TYPE_TO_LAYER

    def test_falls_back_on_malformed_yaml(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        block_dir = tmp_path / "block"
        entity_dir = block_dir / "entities"
        entity_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        (block_dir / "meta-model.yaml").write_text("not: [valid: yaml: structure")

        ont = load_ontology(entity_dir)
        assert ont.source == "defaults"

    def test_partial_yaml_uses_defaults_for_missing_sections(self, tmp_path: Path) -> None:
        block_dir = tmp_path / "block"
        entity_dir = block_dir / "entities"
        entity_dir.mkdir(parents=True)

        yaml_content = textwrap.dedent("""\
            entity_types:
              system:
                layer: structural
        """)
        (block_dir / "meta-model.yaml").write_text(yaml_content)

        ont = load_ontology(entity_dir)
        assert ont.get_layer("system") == "structural"
        assert ont.relationship_fields == DEFAULT_RELATIONSHIP_FIELDS

    def test_custom_types_get_correct_layers(self, tmp_path: Path) -> None:
        block_dir = tmp_path / "block"
        entity_dir = block_dir / "entities"
        entity_dir.mkdir(parents=True)

        yaml_content = textwrap.dedent("""\
            entity_types:
              constitution-business:
                layer: decision
              lifecycle:
                layer: behavioral
              vision:
                layer: strategic

            relationship_fields:
              - depends_on
        """)
        (block_dir / "meta-model.yaml").write_text(yaml_content)

        ont = load_ontology(entity_dir)
        assert ont.get_layer("constitution-business") == "decision"
        assert ont.get_layer("lifecycle") == "behavioral"
        assert ont.get_layer("vision") == "strategic"
        assert ont.get_layer("system") == "unknown"


class TestBackendWithOntology:
    def _make_entity_file(self, entity_dir: Path, type_name: str, entity_id: str, extra_fm: str = "") -> None:
        type_dir = entity_dir / type_name
        type_dir.mkdir(parents=True, exist_ok=True)
        content = f"---\ntype: {type_name}\nid: {entity_id}\nname: {entity_id.replace('-', ' ').title()}\ndescription: Test entity\nstatus: active\n{extra_fm}---\n\n# {entity_id}\n\nTest body.\n"
        (type_dir / f"{entity_id}.md").write_text(content)

    def test_allowlist_filters_metadata(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from context_blocks.retrieval.backend import InMemoryBackend

        monkeypatch.chdir(tmp_path)
        block_dir = tmp_path / "block"
        entity_dir = block_dir / "entities"
        block_dir.mkdir(parents=True)

        yaml_content = textwrap.dedent("""\
            entity_types:
              system:
                layer: structural

            relationship_fields:
              - related_systems
              - depends_on
        """)
        (block_dir / "meta-model.yaml").write_text(yaml_content)

        self._make_entity_file(entity_dir, "system", "my-system",
                               "make_or_buy: buy\nsource: Archimate\nrelated_systems:\n  - other-system\n")

        backend = InMemoryBackend()
        backend.load_from_entity_dir(entity_dir)

        entity = backend.entities["my-system"]
        rel_types = [r["type"] for r in entity.relationships]
        assert "related_systems" in rel_types
        assert "make_or_buy" not in rel_types
        assert "source" not in rel_types
        assert len(entity.relationships) == 1

    def test_default_ontology_preserves_existing_behavior(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from context_blocks.retrieval.backend import InMemoryBackend

        monkeypatch.chdir(tmp_path)
        entity_dir = tmp_path / "block" / "entities"

        self._make_entity_file(entity_dir, "system", "test-system",
                               "related_to:\n  - other-system\ndepends_on:\n  - platform-x\n")

        backend = InMemoryBackend()
        backend.load_from_entity_dir(entity_dir)

        entity = backend.entities["test-system"]
        rel_types = [r["type"] for r in entity.relationships]
        assert "related_to" in rel_types
        assert "depends_on" in rel_types
        assert len(entity.relationships) == 2
