"""Tests for the Studio API (block create/list/inspect)."""

import textwrap
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from context_blocks.studio_api import create_studio_app


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    return TestClient(create_studio_app(root=tmp_path))


def _custom_ontology_yaml() -> str:
    return textwrap.dedent("""\
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


# ── health / list ────────────────────────────────────────────────────────────


def test_health_reports_root_and_zero_blocks(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["blocks"] == 0


def test_list_blocks_empty(client: TestClient) -> None:
    resp = client.get("/blocks")
    assert resp.status_code == 200
    assert resp.json() == []


# ── create (default ontology) ────────────────────────────────────────────────


def test_create_default_block(client: TestClient, tmp_path: Path) -> None:
    resp = client.post("/blocks", json={"name": "cost-control", "description": "CC block"})
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["name"] == "cost-control"
    assert body["ontology"] == "default"
    # Default ontology carries the built-in 18 types.
    assert "system" in body["ontology_detail"]["types"]

    # Block dir + engine scaffolding exist (identical to `cb init`).
    block_dir = tmp_path / "cost-control"
    assert (block_dir / "block.yaml").exists()
    assert (block_dir / "entities").is_dir()
    assert (block_dir / "extractions").is_dir()
    # Registered in blocks.yaml + project marker written.
    assert (tmp_path / "blocks.yaml").exists()
    assert (tmp_path / ".contextblocks").exists()


def test_created_block_appears_in_list(client: TestClient) -> None:
    client.post("/blocks", json={"name": "alpha"})
    names = [b["name"] for b in client.get("/blocks").json()]
    assert names == ["alpha"]


# ── create (custom ontology + seed) ──────────────────────────────────────────


def test_create_block_with_inline_ontology(client: TestClient, tmp_path: Path) -> None:
    resp = client.post(
        "/blocks",
        json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    # Block references the written meta-model file.
    assert body["ontology"] == "incidents/meta-model.yaml"
    # Ontology reflects the custom types, not the defaults.
    types = body["ontology_detail"]["types"]
    assert "incident" in types and "service" in types
    assert "system" not in types
    # The meta-model file was actually written into the block dir.
    assert (tmp_path / "incidents" / "meta-model.yaml").exists()


def test_create_block_with_inline_seed(client: TestClient, tmp_path: Path) -> None:
    resp = client.post(
        "/blocks",
        json={"name": "with-seed", "seed_context": "# Seed\n\nBounded context orientation."},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["seed_context"] == "with-seed/seed-context.md"
    seed_file = tmp_path / "with-seed" / "seed-context.md"
    assert seed_file.exists()
    assert "Bounded context orientation." in seed_file.read_text()


def test_create_block_rejects_invalid_ontology_yaml(client: TestClient, tmp_path: Path) -> None:
    resp = client.post(
        "/blocks",
        json={"name": "bad-onto", "ontology_yaml": "just a scalar string"},
    )
    assert resp.status_code == 422
    # Nothing should have been created.
    assert not (tmp_path / "bad-onto").exists()


# ── get ──────────────────────────────────────────────────────────────────────


def test_get_block_returns_detail(client: TestClient) -> None:
    client.post("/blocks", json={"name": "gamma", "label": "Gamma Block"})
    resp = client.get("/blocks/gamma")
    assert resp.status_code == 200
    body = resp.json()
    assert body["label"] == "Gamma Block"
    assert body["output_dir"].endswith("/gamma")
    assert "layers" in body["ontology_detail"]


def test_get_unknown_block_404(client: TestClient) -> None:
    assert client.get("/blocks/nope").status_code == 404


# ── validation / conflicts ───────────────────────────────────────────────────


def test_create_invalid_name_422(client: TestClient) -> None:
    resp = client.post("/blocks", json={"name": "Not Kebab Case"})
    assert resp.status_code == 422


def test_create_duplicate_409(client: TestClient) -> None:
    client.post("/blocks", json={"name": "dup"})
    resp = client.post("/blocks", json={"name": "dup"})
    assert resp.status_code == 409


# ── add entity ───────────────────────────────────────────────────────────────


def _incident_entity_md(**overrides: object) -> str:
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


def test_add_entity_to_custom_block(client: TestClient, tmp_path: Path) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})
    resp = client.post(
        "/blocks/incidents/entities",
        json={"content": _incident_entity_md()},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["id"] == "checkout-outage"
    assert body["type"] == "incident"
    # Routed to the custom directory declared in the ontology.
    assert body["path"] == "entities/incidents/checkout-outage.md"
    written = tmp_path / "incidents" / "entities" / "incidents" / "checkout-outage.md"
    assert written.exists()
    assert "Checkout was down" in written.read_text()


def test_add_entity_to_default_block_routes_by_type(client: TestClient, tmp_path: Path) -> None:
    client.post("/blocks", json={"name": "plain"})
    system_md = "\n".join(
        [
            "---",
            "type: system",
            "id: payments-api",
            "name: Payments API",
            "description: Handles payments",
            "status: active",
            "---",
            "",
            "# Payments API",
        ]
    )
    resp = client.post("/blocks/plain/entities", json={"content": system_md})
    assert resp.status_code == 201, resp.text
    # Default meta-model routes 'system' -> 'systems'.
    assert resp.json()["path"] == "entities/systems/payments-api.md"


def test_add_entity_invalid_frontmatter_422(client: TestClient, tmp_path: Path) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})
    resp = client.post(
        "/blocks/incidents/entities",
        json={"content": _incident_entity_md(type="banana")},
    )
    assert resp.status_code == 422
    # Nothing written.
    assert not (tmp_path / "incidents" / "entities" / "banana").exists()


def test_add_entity_expected_id_mismatch_422(client: TestClient) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})
    resp = client.post(
        "/blocks/incidents/entities",
        json={"content": _incident_entity_md(), "id": "some-other-id"},
    )
    assert resp.status_code == 422


def test_add_entity_unknown_block_404(client: TestClient) -> None:
    resp = client.post("/blocks/ghost/entities", json={"content": _incident_entity_md()})
    assert resp.status_code == 404


def test_add_duplicate_entity_409(client: TestClient) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})
    first = client.post("/blocks/incidents/entities", json={"content": _incident_entity_md()})
    assert first.status_code == 201
    second = client.post("/blocks/incidents/entities", json={"content": _incident_entity_md()})
    assert second.status_code == 409
