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


def test_add_entity_with_custom_metadata_returns_warnings(client: TestClient) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})
    # `owner` is neither a standard field nor an ontology relationship → allowed, warned.
    resp = client.post(
        "/blocks/incidents/entities",
        json={"content": _incident_entity_md(owner="raj")},
    )
    assert resp.status_code == 201, resp.text
    assert any("owner" in w for w in resp.json()["warnings"])


# ── bulk add entities ─────────────────────────────────────────────────────────


def _system_md(eid: str, name: str = "Sys", desc: str = "d") -> str:
    return "\n".join(
        [
            "---",
            "type: system",
            f"id: {eid}",
            f"name: {name}",
            f"description: {desc}",
            "status: active",
            "---",
            "",
            f"# {name}",
        ]
    )


def test_bulk_add_creates_all(client: TestClient, tmp_path: Path) -> None:
    client.post("/blocks", json={"name": "plain"})
    resp = client.post(
        "/blocks/plain/entities/bulk",
        json={
            "entities": [
                {"content": _system_md("sys-a")},
                {"content": _system_md("sys-b")},
                {"content": _system_md("sys-c")},
            ]
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert (body["created"], body["skipped"], body["failed"]) == (3, 0, 0)
    assert {r["status"] for r in body["results"]} == {"created"}
    assert (tmp_path / "plain" / "entities" / "systems" / "sys-a.md").exists()
    assert len(client.get("/blocks/plain/entities").json()) == 3


def test_bulk_reports_invalid_alongside_valid(client: TestClient) -> None:
    client.post("/blocks", json={"name": "plain"})
    bad = _system_md("bad").replace("type: system", "type: banana")
    resp = client.post(
        "/blocks/plain/entities/bulk",
        json={"entities": [{"content": _system_md("good")}, {"content": bad}]},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["created"] == 1
    assert body["failed"] == 1
    fails = [r for r in body["results"] if r["status"] == "failed"]
    assert fails and fails[0]["errors"]


def test_bulk_on_conflict_skip_keeps_original(client: TestClient, tmp_path: Path) -> None:
    client.post("/blocks", json={"name": "plain"})
    client.post("/blocks/plain/entities", json={"content": _system_md("dup", name="Original")})
    resp = client.post(
        "/blocks/plain/entities/bulk",
        json={
            "on_conflict": "skip",
            "entities": [
                {"content": _system_md("dup", name="New")},
                {"content": _system_md("fresh")},
            ],
        },
    )
    body = resp.json()
    assert (body["created"], body["skipped"], body["failed"]) == (1, 1, 0)
    dup = tmp_path / "plain" / "entities" / "systems" / "dup.md"
    assert "Original" in dup.read_text()


def test_bulk_on_conflict_error_by_default(client: TestClient) -> None:
    client.post("/blocks", json={"name": "plain"})
    client.post("/blocks/plain/entities", json={"content": _system_md("dup")})
    resp = client.post(
        "/blocks/plain/entities/bulk",
        json={"entities": [{"content": _system_md("dup")}]},
    )
    body = resp.json()
    assert body["failed"] == 1
    assert body["created"] == 0


def test_bulk_on_conflict_overwrite_replaces(client: TestClient, tmp_path: Path) -> None:
    client.post("/blocks", json={"name": "plain"})
    client.post("/blocks/plain/entities", json={"content": _system_md("dup", name="Original")})
    resp = client.post(
        "/blocks/plain/entities/bulk",
        json={"on_conflict": "overwrite", "entities": [{"content": _system_md("dup", name="Replaced")}]},
    )
    assert resp.json()["created"] == 1
    assert "Replaced" in (tmp_path / "plain" / "entities" / "systems" / "dup.md").read_text()


def test_bulk_duplicate_id_within_batch(client: TestClient) -> None:
    client.post("/blocks", json={"name": "plain"})
    resp = client.post(
        "/blocks/plain/entities/bulk",
        json={
            "entities": [
                {"content": _system_md("twin")},
                {"content": _system_md("twin", name="Second")},
            ]
        },
    )
    body = resp.json()
    assert body["created"] == 1
    assert body["failed"] == 1


def test_bulk_unknown_block_404(client: TestClient) -> None:
    resp = client.post(
        "/blocks/ghost/entities/bulk", json={"entities": [{"content": _system_md("x")}]}
    )
    assert resp.status_code == 404


# ── list entities ────────────────────────────────────────────────────────────


def test_list_entities_empty_for_new_block(client: TestClient) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})
    resp = client.get("/blocks/incidents/entities")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_entities_after_add(client: TestClient) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})
    client.post("/blocks/incidents/entities", json={"content": _incident_entity_md()})
    client.post(
        "/blocks/incidents/entities",
        json={"content": _incident_entity_md(id="db-failover", name="DB Failover")},
    )
    resp = client.get("/blocks/incidents/entities")
    assert resp.status_code == 200
    items = resp.json()
    by_id = {i["id"]: i for i in items}
    assert set(by_id) == {"checkout-outage", "db-failover"}
    assert by_id["checkout-outage"]["type"] == "incident"
    assert by_id["checkout-outage"]["name"] == "Checkout Outage"
    assert by_id["checkout-outage"]["path"] == "entities/incidents/checkout-outage.md"


def test_list_entities_unknown_block_404(client: TestClient) -> None:
    assert client.get("/blocks/ghost/entities").status_code == 404


# ── artifacts (non-md files) ─────────────────────────────────────────────────


def _make_block(client: TestClient) -> None:
    client.post("/blocks", json={"name": "incidents", "ontology_yaml": _custom_ontology_yaml()})


def test_upload_and_get_artifact(client: TestClient, tmp_path: Path) -> None:
    _make_block(client)
    resp = client.post(
        "/blocks/incidents/artifacts",
        files={"file": ("arch.drawio", b"<mxfile/>", "application/xml")},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["filename"] == "arch.drawio"
    assert body["path"] == "artifacts/arch.drawio"
    assert body["content_type"] == "application/xml"
    assert (tmp_path / "incidents" / "artifacts" / "arch.drawio").exists()

    # Raw serve returns the bytes + content-type (works for binary too).
    raw = client.get("/blocks/incidents/artifacts/arch.drawio")
    assert raw.status_code == 200
    assert raw.content == b"<mxfile/>"
    assert raw.headers["content-type"].startswith("application/xml")


def test_upload_binary_image_artifact(client: TestClient) -> None:
    _make_block(client)
    png = b"\x89PNG\r\n\x1a\n\x00\x00binary"
    client.post("/blocks/incidents/artifacts", files={"file": ("shot.png", png, "image/png")})
    raw = client.get("/blocks/incidents/artifacts/shot.png")
    assert raw.status_code == 200
    assert raw.content == png
    assert raw.headers["content-type"].startswith("image/png")


def test_list_artifacts(client: TestClient) -> None:
    _make_block(client)
    client.post("/blocks/incidents/artifacts", files={"file": ("a.png", b"x", "image/png")})
    client.post("/blocks/incidents/artifacts", files={"file": ("b.bpmn", b"<x/>", "application/xml")})
    items = client.get("/blocks/incidents/artifacts").json()
    assert {i["filename"] for i in items} == {"a.png", "b.bpmn"}


def test_upload_disallowed_type_415(client: TestClient, tmp_path: Path) -> None:
    _make_block(client)
    resp = client.post(
        "/blocks/incidents/artifacts",
        files={"file": ("notes.md", b"# hi", "text/markdown")},
    )
    assert resp.status_code == 415
    assert not (tmp_path / "incidents" / "artifacts").exists()


def test_artifact_endpoints_unknown_block_404(client: TestClient) -> None:
    assert (
        client.post("/blocks/ghost/artifacts", files={"file": ("a.png", b"x", "image/png")}).status_code
        == 404
    )
    assert client.get("/blocks/ghost/artifacts").status_code == 404
    assert client.get("/blocks/ghost/artifacts/a.png").status_code == 404


def test_get_missing_artifact_404(client: TestClient) -> None:
    _make_block(client)
    assert client.get("/blocks/incidents/artifacts/nope.png").status_code == 404


# ── graph ────────────────────────────────────────────────────────────────────

_SERVICE_MD = (
    "---\ntype: service\nid: payments-service\nname: Payments Service\n"
    "description: Handles payments\nstatus: active\n---\n\n# Payments Service\n"
)


def test_block_graph(client: TestClient) -> None:
    _make_block(client)
    client.post(
        "/blocks/incidents/entities",
        json={"content": _incident_entity_md(affects="[payments-service]")},
    )
    client.post("/blocks/incidents/entities", json={"content": _SERVICE_MD})

    resp = client.get("/blocks/incidents/graph")
    assert resp.status_code == 200
    g = resp.json()

    by_id = {n["id"]: n for n in g["nodes"]}
    assert set(by_id) == {"checkout-outage", "payments-service"}

    # edge built from the ontology relationship field `affects`
    assert any(
        e["source"] == "checkout-outage" and e["target"] == "payments-service" and e["type"] == "affects"
        for e in g["edges"]
    )
    # degree counters
    assert by_id["checkout-outage"]["outgoing_count"] == 1
    assert by_id["payments-service"]["incoming_count"] == 1

    # node metadata for the graph view
    assert by_id["checkout-outage"]["type_label"] == "Incidents"
    assert by_id["checkout-outage"]["layer"] == "behavioral"
    assert by_id["checkout-outage"]["layer_color"].startswith("#")

    # layers + type legend
    assert {l["key"] for l in g["layers"]} >= {"behavioral", "structural"}
    assert {t["key"] for t in g["entity_types"]} == {"incident", "service"}


def test_block_graph_empty_block(client: TestClient) -> None:
    client.post("/blocks", json={"name": "empty"})
    g = client.get("/blocks/empty/graph").json()
    assert g["nodes"] == []
    assert g["edges"] == []


def test_block_graph_unknown_block_404(client: TestClient) -> None:
    assert client.get("/blocks/ghost/graph").status_code == 404


# ── ontology (schema blueprint) ──────────────────────────────────────────────


def test_block_ontology(client: TestClient) -> None:
    _make_block(client)
    resp = client.get("/blocks/incidents/ontology")
    assert resp.status_code == 200
    body = resp.json()
    # Full schema — all declared types, independent of whether entities exist.
    by_type = {t["key"]: t for t in body["types"]}
    assert set(by_type) == {"incident", "service"}
    assert by_type["incident"]["layer"] == "behavioral"
    assert {l["key"] for l in body["layers"]} == {"behavioral", "structural"}
    assert set(body["relationship_fields"]) == {"affects", "resolved_by"}


def test_default_block_ontology_has_18_types(client: TestClient) -> None:
    client.post("/blocks", json={"name": "plain"})
    body = client.get("/blocks/plain/ontology").json()
    assert len(body["types"]) == 18
    assert "system" in {t["key"] for t in body["types"]}


def test_block_ontology_unknown_block_404(client: TestClient) -> None:
    assert client.get("/blocks/ghost/ontology").status_code == 404


# ── metrics ───────────────────────────────────────────────────────────────────


def test_metrics_endpoint_aggregates_efforts_and_changes(client: TestClient) -> None:
    from context_blocks import tracing

    assert client.post("/blocks", json={"name": "cc", "description": "d"}).status_code == 201
    out = Path([b for b in client.get("/blocks").json() if b["name"] == "cc"][0]["output_dir"])

    # Adding an entity logs a change event (actor recorded).
    md = "---\ntype: system\nid: svc-a\nname: Svc A\ndescription: d\nstatus: active\n---\n\n# Svc A\n"
    assert client.post("/blocks/cc/entities", json={"content": md, "actor": "luffy"}).status_code == 201

    # Simulate one work-effort: one hit, one gap.
    wid = tracing.begin(out, "cc", "triage svc-a", agent="luffy")
    tracing.log_call(out, wid, "get_entity", {"entity_id": "svc-a"}, "got svc-a", is_gap=False)
    tracing.log_call(out, wid, "get_entity", {"entity_id": "missing"}, "not found", is_gap=True)
    tracing.end(out, wid, "resolved")

    m = client.get("/blocks/cc/metrics").json()
    we = m["work_efforts"]
    assert (we["total"], we["total_calls"], we["total_gaps"], we["gap_rate"]) == (1, 2, 1, 0.5)
    assert {"entity_id": "svc-a", "hits": 1} in m["top_entities"]
    assert any(g["args"].get("entity_id") == "missing" for g in m["gaps"])
    assert m["changes"]["total"] >= 1
    assert m["changes"]["by_action"].get("created", 0) >= 1
    assert any(a["actor"] == "luffy" for a in m["changes"]["by_actor"])


def test_metrics_404_for_unknown_block(client: TestClient) -> None:
    assert client.get("/blocks/nope/metrics").status_code == 404
