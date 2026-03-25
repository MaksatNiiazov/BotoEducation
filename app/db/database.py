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
    with get_connection() as conn:
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(links)")}
        if columns and "user_id" not in columns:
            conn.executescript(
                """
                ALTER TABLE links RENAME TO links_legacy;
                CREATE TABLE links (
                  code TEXT PRIMARY KEY,
                  user_id TEXT NOT NULL,
                  url TEXT NOT NULL,
                  created_at TEXT NOT NULL
                );
                INSERT INTO links (code, user_id, url, created_at)
                SELECT code, 'anonymous', url, created_at
                FROM links_legacy;
                DROP TABLE links_legacy;
                """
            )

        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS links (
              code TEXT PRIMARY KEY,
              user_id TEXT NOT NULL,
              url TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id);
            """
        )
        conn.commit()
