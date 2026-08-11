from pathlib import Path

from context_blocks import temporal
from context_blocks.importer import bulk_add_entities
from context_blocks.ontology import Ontology


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


def test_bulk_writes_all_and_routes_by_type(tmp_path: Path) -> None:
    res = bulk_add_entities(Ontology(), tmp_path, [(_system_md("a"), None), (_system_md("b"), None)])
    assert (res.created, res.skipped, res.failed) == (2, 0, 0)
    assert (tmp_path / "entities" / "systems" / "a.md").exists()
    assert (tmp_path / "entities" / "systems" / "b.md").exists()


def test_bulk_stamps_temporal_and_records_events(tmp_path: Path) -> None:
    bulk_add_entities(Ontology(), tmp_path, [(_system_md("a"), None)], actor="luffy")
    written = (tmp_path / "entities" / "systems" / "a.md").read_text()
    assert "created_at:" in written and 'updated_by: "luffy"' in written
    events = temporal.get_events(tmp_path)
    assert len(events) == 1
    assert (events[0]["entity_id"], events[0]["action"], events[0]["actor"]) == ("a", "created", "luffy")


def test_overwrite_preserves_created_at_and_logs_update(tmp_path: Path) -> None:
    bulk_add_entities(Ontology(), tmp_path, [(_system_md("dup", name="Original"), None)], actor="import")
    birth = temporal.read_created_at((tmp_path / "entities" / "systems" / "dup.md").read_text())
    bulk_add_entities(
        Ontology(), tmp_path, [(_system_md("dup", name="Replaced"), None)],
        on_conflict="overwrite", actor="luffy",
    )
    after = (tmp_path / "entities" / "systems" / "dup.md").read_text()
    assert temporal.read_created_at(after) == birth  # birth carried across overwrite
    assert 'updated_by: "luffy"' in after
    actions = [e["action"] for e in temporal.get_events(tmp_path)]
    assert actions == ["updated", "created"]  # newest first


def test_invalid_reported_not_written(tmp_path: Path) -> None:
    bad = _system_md("bad").replace("type: system", "type: banana")
    res = bulk_add_entities(Ontology(), tmp_path, [(_system_md("good"), None), (bad, None)])
    assert res.created == 1
    assert res.failed == 1
    fails = [r for r in res.results if r.status == "failed"]
    assert fails and fails[0].errors
    assert not (tmp_path / "entities" / "systems" / "bad.md").exists()


def test_conflict_skip_keeps_original(tmp_path: Path) -> None:
    bulk_add_entities(Ontology(), tmp_path, [(_system_md("dup", name="Original"), None)])
    res = bulk_add_entities(
        Ontology(), tmp_path, [(_system_md("dup", name="New"), None)], on_conflict="skip"
    )
    assert res.skipped == 1
    assert "Original" in (tmp_path / "entities" / "systems" / "dup.md").read_text()


def test_conflict_overwrite_replaces(tmp_path: Path) -> None:
    bulk_add_entities(Ontology(), tmp_path, [(_system_md("dup", name="Original"), None)])
    res = bulk_add_entities(
        Ontology(), tmp_path, [(_system_md("dup", name="Replaced"), None)], on_conflict="overwrite"
    )
    assert res.created == 1
    assert "Replaced" in (tmp_path / "entities" / "systems" / "dup.md").read_text()


def test_conflict_error_by_default(tmp_path: Path) -> None:
    bulk_add_entities(Ontology(), tmp_path, [(_system_md("dup"), None)])
    res = bulk_add_entities(Ontology(), tmp_path, [(_system_md("dup"), None)])
    assert res.failed == 1
    assert res.created == 0


def test_duplicate_id_within_batch(tmp_path: Path) -> None:
    res = bulk_add_entities(
        Ontology(), tmp_path, [(_system_md("t"), None), (_system_md("t", name="Second"), None)]
    )
    assert res.created == 1
    assert res.failed == 1


def test_expected_id_mismatch_fails(tmp_path: Path) -> None:
    res = bulk_add_entities(Ontology(), tmp_path, [(_system_md("real"), "different")])
    assert res.failed == 1
    assert not (tmp_path / "entities" / "systems" / "real.md").exists()
