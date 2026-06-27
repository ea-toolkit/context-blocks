"""LLM call tracing — captures every prompt, response, and metadata.

Stored in SQLite for easy querying and debugging.
No external dependencies beyond Python stdlib + pydantic.
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)

# Module-level database path — set by init_trace_db()
_db_path: Path | None = None


def init_trace_db(output_dir: Path) -> None:
    """Initialize the trace database in the output directory.

    Args:
        output_dir: Directory where the trace DB will be stored.
    """
    global _db_path
    output_dir.mkdir(parents=True, exist_ok=True)
    _db_path = output_dir / ".context-blocks-traces.db"

    conn = sqlite3.connect(str(_db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS llm_traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            task TEXT NOT NULL,
            document TEXT,
            model TEXT NOT NULL,
            system_prompt TEXT,
            user_prompt TEXT NOT NULL,
            response_raw TEXT,
            response_model TEXT,
            prompt_tokens_est INTEGER,
            response_tokens_est INTEGER,
            duration_ms INTEGER,
            status TEXT NOT NULL,
            error TEXT
        )
    """)
    conn.commit()
    conn.close()

    logger.debug("trace_db_initialized", path=str(_db_path))


def save_trace(
    task: str,
    document: str | None,
    model: str,
    system_prompt: str | None,
    user_prompt: str,
    response_raw: str | None,
    response_model: str | None,
    prompt_tokens_est: int,
    response_tokens_est: int,
    duration_ms: int,
    status: str,
    error: str | None = None,
) -> None:
    """Save a single LLM call trace to the database.

    Args:
        task: Which task made this call (scan, analyze, gaps).
        document: Document filename being processed (if applicable).
        model: LLM model used.
        system_prompt: System prompt sent.
        user_prompt: User prompt sent.
        response_raw: Raw response text from LLM.
        response_model: Pydantic model name used for structured output.
        prompt_tokens_est: Estimated input tokens.
        response_tokens_est: Estimated output tokens.
        duration_ms: Call duration in milliseconds.
        status: "success" or "error".
        error: Error message if status is "error".
    """
    if _db_path is None:
        logger.warning("trace_db_not_initialized", task=task)
        return

    try:
        conn = sqlite3.connect(str(_db_path))
        conn.execute(
            """
            INSERT INTO llm_traces
            (timestamp, task, document, model, system_prompt, user_prompt,
             response_raw, response_model, prompt_tokens_est, response_tokens_est,
             duration_ms, status, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                task,
                document,
                model,
                system_prompt,
                user_prompt,
                response_raw,
                response_model,
                prompt_tokens_est,
                response_tokens_est,
                duration_ms,
                status,
                error,
            ),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error("trace_save_failed", error=str(e))


def get_traces(
    output_dir: Path,
    task: str | None = None,
    document: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """Query traces from the database.

    Args:
        output_dir: Directory containing the trace DB.
        task: Filter by task name (optional).
        document: Filter by document filename (optional).
        limit: Max number of traces to return.

    Returns:
        List of trace records as dicts.
    """
    db_path = output_dir / ".context-blocks-traces.db"
    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    query = "SELECT * FROM llm_traces WHERE 1=1"
    params: list = []

    if task:
        query += " AND task = ?"
        params.append(task)
    if document:
        query += " AND document = ?"
        params.append(document)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_trace_summary(output_dir: Path) -> dict:
    """Get a summary of all traces — total calls, tokens, duration.

    Args:
        output_dir: Directory containing the trace DB.

    Returns:
        Summary dict with counts and totals.
    """
    db_path = output_dir / ".context-blocks-traces.db"
    if not db_path.exists():
        return {"total_calls": 0}

    conn = sqlite3.connect(str(db_path))

    row = conn.execute("""
        SELECT
            COUNT(*) as total_calls,
            SUM(prompt_tokens_est) as total_prompt_tokens,
            SUM(response_tokens_est) as total_response_tokens,
            SUM(duration_ms) as total_duration_ms,
            COUNT(CASE WHEN status = 'error' THEN 1 END) as errors
        FROM llm_traces
    """).fetchone()

    conn.close()

    return {
        "total_calls": row[0] or 0,
        "total_prompt_tokens": row[1] or 0,
        "total_response_tokens": row[2] or 0,
        "total_duration_ms": row[3] or 0,
        "errors": row[4] or 0,
    }
