"""Work-effort tracing — the demand log.

Groups an agent's many KB calls under ONE work-effort (one intent), so we can
see what agents actually ask, where they hit gaps, and how a single unit of work
played out — search → get → resolve → gap → outcome, all under one id.

Stored per-block in SQLite (`<output_dir>/.work-effort-traces.db`). This is the
*demand signal* that drives curation, not just observability: the misses are the
gaps, and the recurring intents are what to curate next.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

DB_NAME = ".work-effort-traces.db"


def _db_path(output_dir: Path | str) -> Path:
    return Path(output_dir) / DB_NAME


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect(output_dir: Path | str) -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path(output_dir))
    conn.execute(
        """CREATE TABLE IF NOT EXISTS work_efforts (
            id TEXT PRIMARY KEY, block TEXT, agent TEXT, intent TEXT,
            started_at TEXT, ended_at TEXT, outcome TEXT,
            call_count INTEGER DEFAULT 0, gap_count INTEGER DEFAULT 0)"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS work_effort_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT, work_effort_id TEXT, seq INTEGER,
            tool TEXT, args TEXT, summary TEXT, is_gap INTEGER, at TEXT)"""
    )
    return conn


def begin(output_dir: Path | str, block: str, intent: str, agent: str = "") -> str:
    """Open a work-effort (one intent) and return its id."""
    wid = "we-" + uuid.uuid4().hex[:12]
    conn = _connect(output_dir)
    conn.execute(
        "INSERT INTO work_efforts (id, block, agent, intent, started_at) VALUES (?,?,?,?,?)",
        (wid, block, agent, intent, _now()),
    )
    conn.commit()
    conn.close()
    return wid


def log_call(
    output_dir: Path | str,
    work_effort_id: str,
    tool: str,
    args: dict,
    summary: str,
    is_gap: bool,
) -> None:
    """Append one call (with its hit/miss) to a work-effort."""
    conn = _connect(output_dir)
    seq = conn.execute(
        "SELECT COALESCE(MAX(seq),0)+1 FROM work_effort_calls WHERE work_effort_id=?",
        (work_effort_id,),
    ).fetchone()[0]
    conn.execute(
        "INSERT INTO work_effort_calls (work_effort_id, seq, tool, args, summary, is_gap, at)"
        " VALUES (?,?,?,?,?,?,?)",
        (work_effort_id, seq, tool, json.dumps(args)[:2000], summary[:1000], 1 if is_gap else 0, _now()),
    )
    conn.execute(
        "UPDATE work_efforts SET call_count=call_count+1, gap_count=gap_count+? WHERE id=?",
        (1 if is_gap else 0, work_effort_id),
    )
    conn.commit()
    conn.close()


def end(output_dir: Path | str, work_effort_id: str, outcome: str = "") -> None:
    """Close a work-effort with an outcome (resolved / escalated / etc.)."""
    conn = _connect(output_dir)
    conn.execute(
        "UPDATE work_efforts SET ended_at=?, outcome=? WHERE id=?",
        (_now(), outcome, work_effort_id),
    )
    conn.commit()
    conn.close()


def get_work_efforts(output_dir: Path | str, limit: int = 50) -> list[dict]:
    """Read recent work-efforts (each with its call-chain) — the demand log."""
    if not _db_path(output_dir).exists():
        return []
    conn = _connect(output_dir)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM work_efforts ORDER BY started_at DESC LIMIT ?", (limit,)
    ).fetchall()
    out = []
    for r in rows:
        calls = conn.execute(
            "SELECT seq, tool, args, summary, is_gap, at FROM work_effort_calls"
            " WHERE work_effort_id=? ORDER BY seq",
            (r["id"],),
        ).fetchall()
        d = dict(r)
        d["calls"] = [dict(c) for c in calls]
        out.append(d)
    conn.close()
    return out
