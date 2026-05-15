"""
SQLite storage for scan history and analytics (lightweight).
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Any

from app.config import DATA_DIR, DB_PATH


def init_db() -> None:
    """Create tables if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                input_preview TEXT,
                prediction TEXT,
                confidence REAL,
                threat_level TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def log_scan(
    module: str,
    input_preview: str,
    prediction: str,
    confidence: float,
    threat_level: str,
) -> None:
    """Record a prediction for dashboard analytics."""
    init_db()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO scans (module, input_preview, prediction, confidence, threat_level, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                module,
                input_preview[:200],
                prediction,
                confidence,
                threat_level,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()


def get_scan_stats() -> dict[str, Any]:
    """Aggregate stats for Threat Analytics page."""
    init_db()
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM scans").fetchone()[0]
        by_module = conn.execute(
            "SELECT module, COUNT(*) as cnt FROM scans GROUP BY module"
        ).fetchall()
        by_threat = conn.execute(
            "SELECT threat_level, COUNT(*) as cnt FROM scans GROUP BY threat_level"
        ).fetchall()
        recent = conn.execute(
            "SELECT * FROM scans ORDER BY id DESC LIMIT 20"
        ).fetchall()
    return {
        "total_scans": total,
        "by_module": {r["module"]: r["cnt"] for r in by_module},
        "by_threat": {r["threat_level"]: r["cnt"] for r in by_threat},
        "recent": [dict(r) for r in recent],
    }
