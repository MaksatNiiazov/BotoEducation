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
    log_file_path: str
    thread_pool_workers: int
    jwt_secret: str
    jwt_algorithm: str
    bot_token: str | None
    admin_chat_id: str | None


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_host=_get_env("APP_HOST"),
        app_port=int(_get_env("APP_PORT")),
        database_path=_get_env("DATABASE_PATH"),
        base_url=_get_env("BASE_URL"),
        log_level=_get_env("LOG_LEVEL", "INFO"),
        log_file_path=_get_env("LOG_FILE_PATH", "./logs/app.json.log"),
        thread_pool_workers=int(_get_env("THREAD_POOL_WORKERS", "8")),
        jwt_secret=_get_env("JWT_SECRET"),
        jwt_algorithm=_get_env("JWT_ALGORITHM", "HS256"),
        bot_token=os.getenv("BOT_TOKEN"),
        admin_chat_id=os.getenv("ADMIN_CHAT_ID"),
    )
