"""Tests for temporal metadata + the Context Sourcing event store."""

from pathlib import Path

from context_blocks import temporal

DOC = "\n".join(["---", "type: system", "id: a", "name: A", "status: active", "---", "", "# A"])


class TestStampMarkdown:
    def test_new_adds_all_three_fields(self) -> None:
        out = temporal.stamp_markdown(DOC, "luffy", now="2026-08-11T00:00:00+00:00")
        assert 'created_at: "2026-08-11T00:00:00+00:00"' in out
        assert 'updated_at: "2026-08-11T00:00:00+00:00"' in out
        assert 'updated_by: "luffy"' in out
        assert "# A" in out  # body preserved

    def test_update_preserves_created_refreshes_updated(self) -> None:
        first = temporal.stamp_markdown(DOC, "extraction", now="2026-01-01T00:00:00+00:00")
        second = temporal.stamp_markdown(first, "luffy", now="2026-08-11T00:00:00+00:00")
        assert 'created_at: "2026-01-01T00:00:00+00:00"' in second  # birth kept
        assert 'updated_at: "2026-08-11T00:00:00+00:00"' in second  # refreshed
        assert 'updated_by: "luffy"' in second
        assert second.count("created_at:") == 1  # no duplicate

    def test_created_at_override_used_when_absent(self) -> None:
        out = temporal.stamp_markdown(
            DOC, "import", now="2026-08-11T00:00:00+00:00", created_at="2025-05-05T00:00:00+00:00"
        )
        assert 'created_at: "2025-05-05T00:00:00+00:00"' in out

    def test_no_frontmatter_passthrough(self) -> None:
        assert temporal.stamp_markdown("just text, no fences", "x") == "just text, no fences"

    def test_read_created_at(self) -> None:
        stamped = temporal.stamp_markdown(DOC, "x", now="2026-08-11T00:00:00+00:00")
        assert temporal.read_created_at(stamped) == "2026-08-11T00:00:00+00:00"
        assert temporal.read_created_at(DOC) is None


class TestStampDict:
    def test_sets_and_preserves(self) -> None:
        fm = {"id": "a"}
        temporal.stamp_dict(fm, "extraction", now="2026-01-01T00:00:00+00:00")
        assert fm["created_at"] == "2026-01-01T00:00:00+00:00"
        assert fm["updated_by"] == "extraction"
        # a later stamp keeps created, moves updated
        temporal.stamp_dict(fm, "luffy", now="2026-08-11T00:00:00+00:00")
        assert fm["created_at"] == "2026-01-01T00:00:00+00:00"
        assert fm["updated_at"] == "2026-08-11T00:00:00+00:00"


class TestEventStore:
    def test_record_and_read(self, tmp_path: Path) -> None:
        temporal.record_event(tmp_path, "wom-connector", "service", "created", "luffy",
                              summary="WOM Connector", work_effort_id="we-123")
        temporal.record_event(tmp_path, "wom-connector", "service", "updated", "billy")
        events = temporal.get_events(tmp_path)
        assert len(events) == 2
        assert events[0]["action"] == "updated"  # newest first
        assert events[0]["actor"] == "billy"
        assert events[1]["work_effort_id"] == "we-123"

    def test_filter_by_entity(self, tmp_path: Path) -> None:
        temporal.record_event(tmp_path, "a", "system", "created", "x")
        temporal.record_event(tmp_path, "b", "system", "created", "x")
        assert len(temporal.get_events(tmp_path, entity_id="a")) == 1

    def test_empty_when_no_db(self, tmp_path: Path) -> None:
        assert temporal.get_events(tmp_path) == []
