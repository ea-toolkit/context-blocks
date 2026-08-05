"""Tests for entity-frontmatter validation against a block's ontology."""

import textwrap
from pathlib import Path

import pytest

from context_blocks.ontology import Ontology, load_ontology_from_file
from context_blocks.validation import (
    parse_frontmatter,
    validate_entity_frontmatter,
)


def _custom_ontology(tmp_path: Path) -> Ontology:
    (tmp_path / "meta-model.yaml").write_text(
        textwrap.dedent("""\
            layers:
              structural: { label: Structural }
              behavioral: { label: Behavioral }
            entity_types:
              incident: { layer: behavioral, directory: incidents, label: Incidents }
              service:  { layer: structural, directory: services, label: Services }
            relationship_fields:
              - affects
              - resolved_by
        """)
    )
    return load_ontology_from_file(tmp_path / "meta-model.yaml")


def _entity_md(**overrides: object) -> str:
    fields = {
        "type": "incident",
        "id": "checkout-outage",
        "name": "Checkout Outage",
        "description": "Checkout was down",
        "status": "active",
    }
    fields.update(overrides)
    lines = ["---"]
    for key, value in fields.items():
        if value is not None:
            lines.append(f"{key}: {value}")
    lines += ["---", "", "# Checkout Outage", "", "## Overview", "", "Body."]
    return "\n".join(lines)


# ── parse_frontmatter ────────────────────────────────────────────────────────


def test_parse_frontmatter_extracts_dict_and_body() -> None:
    fm, body = parse_frontmatter(_entity_md())
    assert fm is not None
    assert fm["type"] == "incident"
    assert body.startswith("# Checkout Outage")


def test_parse_frontmatter_none_when_no_block() -> None:
    fm, body = parse_frontmatter("# Just a heading\n\nNo frontmatter here.")
    assert fm is None


def test_parse_frontmatter_none_when_not_a_mapping() -> None:
    fm, _ = parse_frontmatter("---\n- just\n- a\n- list\n---\nbody")
    assert fm is None


# ── happy path ───────────────────────────────────────────────────────────────


def test_valid_entity_passes(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(), ont)
    assert result.valid
    assert result.errors == []
    assert result.frontmatter["id"] == "checkout-outage"


def test_valid_entity_with_allowed_relationship(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(affects="payments-api"), ont)
    assert result.valid, result.error_messages


# ── failures ─────────────────────────────────────────────────────────────────


def test_missing_frontmatter_fails() -> None:
    result = validate_entity_frontmatter("# no frontmatter", Ontology())
    assert not result.valid
    assert any(e.field == "frontmatter" for e in result.errors)


def test_missing_required_field_fails(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(name=None), ont)
    assert not result.valid
    assert any(e.field == "name" for e in result.errors)


def test_unknown_type_fails(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(type="banana"), ont)
    assert not result.valid
    assert any(e.field == "type" for e in result.errors)


def test_default_type_rejected_by_custom_ontology(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    # "system" is a default type but not in this custom ontology.
    result = validate_entity_frontmatter(_entity_md(type="system"), ont)
    assert not result.valid
    assert any(e.field == "type" for e in result.errors)


def test_non_kebab_id_fails(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(id="Checkout_Outage"), ont)
    assert not result.valid
    assert any(e.field == "id" for e in result.errors)


def test_id_mismatch_with_expected_fails(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(), ont, expected_id="different-id")
    assert not result.valid
    assert any(e.field == "id" for e in result.errors)


def test_expected_id_match_passes(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(), ont, expected_id="checkout-outage")
    assert result.valid, result.error_messages


def test_invalid_status_fails(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(_entity_md(status="live"), ont)
    assert not result.valid
    assert any(e.field == "status" for e in result.errors)


def test_unknown_relationship_field_fails(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    # "depends_on" is a default relationship field but NOT in this custom ontology.
    result = validate_entity_frontmatter(_entity_md(depends_on="x"), ont)
    assert not result.valid
    assert any(e.field == "depends_on" for e in result.errors)


def test_dangling_relationship_target_is_tolerated(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    # Target 'ghost-service' does not exist, but a valid rel *key* must still pass —
    # broken targets are a health-lint concern, not a validation failure.
    result = validate_entity_frontmatter(_entity_md(resolved_by="ghost-service"), ont)
    assert result.valid, result.error_messages


def test_multiple_errors_all_reported(tmp_path: Path) -> None:
    ont = _custom_ontology(tmp_path)
    result = validate_entity_frontmatter(
        _entity_md(type="banana", status="live", id="Bad_Id"), ont
    )
    fields = {e.field for e in result.errors}
    assert {"type", "status", "id"} <= fields


# ── default ontology ─────────────────────────────────────────────────────────


def test_default_ontology_accepts_default_type_and_rel() -> None:
    md = "\n".join(
        [
            "---",
            "type: system",
            "id: payments-api",
            "name: Payments API",
            "description: Handles payments",
            "status: active",
            "depends_on: [billing-db]",
            "---",
            "",
            "# Payments API",
        ]
    )
    result = validate_entity_frontmatter(md, Ontology())
    assert result.valid, result.error_messages
