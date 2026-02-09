from __future__ import annotations

import logging
import os
import sqlite3
from contextlib import contextmanager

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@contextmanager
def get_connection() -> sqlite3.Connection:
    settings = get_settings()
    db_path = settings.database_path
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    connection = sqlite3.connect(db_path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def init_db() -> None:
    schema = """
    CREATE TABLE IF NOT EXISTS links (
        code TEXT PRIMARY KEY,
        url TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """
    with get_connection() as connection:
        connection.execute(schema)
        connection.commit()
    logger.info("Database schema ensured.")
