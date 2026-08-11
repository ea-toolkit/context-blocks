"""Temporal metadata + Context Sourcing — every persisted change is timestamped and attributed.

Two layers:
  1. Frontmatter stamps (created_at / updated_at / updated_by) so each entity file is
     self-describing about when it was born, last touched, and by whom.
  2. A per-block event store (.context-events.db) recording every create/update as a
     structured event — the queryable Context Sourcing log the metrics dashboard reads
     (frontmatter alone isn't queryable without scanning every file). Each event can be
     linked to the work_effort that caused it, tying a change back to its demand.

Principle: everything we persist gets a timestamp and an author.
"""

from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

TEMPORAL_FIELDS = ("created_at", "updated_at", "updated_by")
EVENTS_DB = ".context-events.db"

_FENCE = "---"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── frontmatter stamping ────────────────────────────────────────────────────

def read_created_at(content: str) -> str | None:
    """Return the created_at value from an entity's frontmatter, or None if absent."""
    lines = content.split("\n")
    fences = [i for i, ln in enumerate(lines) if ln.strip() == _FENCE]
    if len(fences) < 2:
        return None
    for ln in lines[fences[0] + 1 : fences[1]]:
        if ln.split(":", 1)[0].strip() == "created_at" and ":" in ln:
            return ln.split(":", 1)[1].strip().strip('"').strip("'") or None
    return None


def stamp_markdown(
    content: str, actor: str, *, now: str | None = None, created_at: str | None = None
) -> str:
    """Inject/refresh created_at/updated_at/updated_by in an entity's YAML frontmatter,
    preserving the rest of the document verbatim. Keeps an existing created_at (so updates
    don't reset birth); falls back to the `created_at` override (e.g. the prior file's birth
    on overwrite), else now. Refreshes updated_at/updated_by always. Returns content
    unchanged if there's no frontmatter block."""
    now = now or now_iso()
    lines = content.split("\n")
    fences = [i for i, ln in enumerate(lines) if ln.strip() == _FENCE]
    if len(fences) < 2:
        return content
    start, end = fences[0], fences[1]

    created = None
    kept = []
    for ln in lines[start + 1 : end]:
        key = ln.split(":", 1)[0].strip() if ":" in ln else ""
        if key == "created_at":
            created = ln.split(":", 1)[1].strip().strip('"').strip("'")
            continue
        if key in ("updated_at", "updated_by"):
            continue
        kept.append(ln)
    if not created:
        created = created_at or now

    stamp = [
        f'created_at: "{created}"',
        f'updated_at: "{now}"',
        f'updated_by: "{actor}"',
    ]
    new_lines = lines[: start + 1] + kept + stamp + lines[end:]
    return "\n".join(new_lines)


def stamp_dict(frontmatter: dict, actor: str, *, now: str | None = None) -> dict:
    """Stamp a frontmatter dict in place (for builders that assemble a dict, not text)."""
    now = now or now_iso()
    frontmatter.setdefault("created_at", now)
    frontmatter["updated_at"] = now
    frontmatter["updated_by"] = actor
    return frontmatter


# ── event store (Context Sourcing) ──────────────────────────────────────────

def _connect(output_dir: Path | str) -> sqlite3.Connection:
    conn = sqlite3.connect(Path(output_dir) / EVENTS_DB)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS context_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT, entity_id TEXT,
            entity_type TEXT, action TEXT, actor TEXT, work_effort_id TEXT, summary TEXT)"""
    )
    return conn


def record_event(
    output_dir: Path | str,
    entity_id: str,
    entity_type: str,
    action: str,
    actor: str,
    summary: str = "",
    work_effort_id: str = "",
    now: str | None = None,
) -> None:
    """Append one change event (created / updated / deleted) for an entity."""
    conn = _connect(output_dir)
    conn.execute(
        "INSERT INTO context_events (at, entity_id, entity_type, action, actor, work_effort_id, summary)"
        " VALUES (?,?,?,?,?,?,?)",
        (now or now_iso(), entity_id, entity_type, action, actor, work_effort_id, summary[:500]),
    )
    conn.commit()
    conn.close()


def get_events(
    output_dir: Path | str, limit: int = 100, entity_id: str | None = None
) -> list[dict]:
    """Read recent change events (newest first), optionally filtered to one entity."""
    path = Path(output_dir) / EVENTS_DB
    if not path.exists():
        return []
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    query = "SELECT * FROM context_events"
    params: list = []
    if entity_id:
        query += " WHERE entity_id = ?"
        params.append(entity_id)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    rows = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return rows
