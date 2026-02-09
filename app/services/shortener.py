from __future__ import annotations

import logging
import secrets
import sqlite3
import string
from datetime import datetime, timezone
from urllib.parse import urlparse

from app.db.database import get_connection

logger = logging.getLogger(__name__)

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
MAX_RETRIES = 10


class ShortenerError(Exception):
    pass


class InvalidUrlError(ShortenerError):
    pass


class NotFoundError(ShortenerError):
    pass


class StorageError(ShortenerError):
    pass


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    if not parsed.netloc:
        return False
    return True


def _generate_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def create_short_code(url: str) -> str:
    if not is_valid_url(url):
        logger.info("Invalid URL attempt: %s", url)
        raise InvalidUrlError("Invalid URL")

    created_at = datetime.now(timezone.utc).isoformat()
    try:
        with get_connection() as connection:
            for _ in range(MAX_RETRIES):
                code = _generate_code()
                try:
                    connection.execute(
                        "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
                        (code, url, created_at),
                    )
                    connection.commit()
                    logger.info("Short URL created: code=%s url=%s", code, url)
                    return code
                except sqlite3.IntegrityError:
                    continue
    except sqlite3.Error as exc:
        logger.exception("Database error during URL creation.")
        raise StorageError("Database failure") from exc

    logger.error("Failed to generate a unique short code.")
    raise StorageError("Could not generate a unique short code")


def get_original_url(code: str) -> str:
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                "SELECT url FROM links WHERE code = ?",
                (code,),
            )
            row = cursor.fetchone()
    except sqlite3.Error as exc:
        logger.exception("Database error during redirect lookup.")
        raise StorageError("Database failure") from exc

    if row is None:
        logger.info("Short code not found: %s", code)
        raise NotFoundError("Short code not found")

    url = row["url"]
    logger.info("Redirecting code=%s to url=%s", code, url)
    return url
