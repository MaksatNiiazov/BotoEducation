from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager

from app.core.config import get_settings


@contextmanager
def get_connection() -> sqlite3.Connection:
    db_path = get_settings().database_path
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    schema = """
    CREATE TABLE IF NOT EXISTS links (
      code TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      url TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id);
    """
    with get_connection() as conn:
        conn.executescript(schema)
        conn.commit()
