from __future__ import annotations

import secrets
import sqlite3
import string
from datetime import datetime, timezone

from app.db.database import get_connection

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
MAX_RETRIES = 10


class NotFoundError(Exception):
    pass


class StorageError(Exception):
    pass


def _generate_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def create_short_code(user_id: str, url: str) -> str:
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        with get_connection() as conn:
            for _ in range(MAX_RETRIES):
                code = _generate_code()
                try:
                    conn.execute(
                        "INSERT INTO links (code, user_id, url, created_at) VALUES (?, ?, ?, ?)",
                        (code, user_id, url, created_at),
                    )
                    conn.commit()
                    return code
                except sqlite3.IntegrityError:
                    continue
    except sqlite3.Error as exc:
        raise StorageError("Database failure") from exc
    raise StorageError("Could not generate unique code")


def get_original_url(code: str) -> str:
    try:
        with get_connection() as conn:
            row = conn.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
    except sqlite3.Error as exc:
        raise StorageError("Database failure") from exc
    if row is None:
        raise NotFoundError("Short code not found")
    return str(row["url"])


def get_user_links(user_id: str) -> list[dict]:
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT code, url, created_at FROM links WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
    except sqlite3.Error as exc:
        raise StorageError("Database failure") from exc
    return [{"code": r["code"], "url": r["url"], "created_at": r["created_at"]} for r in rows]
