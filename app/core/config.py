from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    app_host: str
    app_port: int
    database_path: str
    base_url: str
    log_level: str


def _get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache
def get_settings() -> Settings:
    app_port_raw = _get_env("APP_PORT")
    try:
        app_port = int(app_port_raw)
    except ValueError as exc:
        raise RuntimeError("APP_PORT must be an integer") from exc

    return Settings(
        app_host=_get_env("APP_HOST"),
        app_port=app_port,
        database_path=_get_env("DATABASE_PATH"),
        base_url=_get_env("BASE_URL"),
        log_level=_get_env("LOG_LEVEL"),
    )
