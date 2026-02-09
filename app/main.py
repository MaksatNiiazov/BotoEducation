from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.database import init_db

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        settings = get_settings()
        configure_logging(settings.log_level)
        logger.info("App startup: host=%s port=%s", settings.app_host, settings.app_port)
        init_db()
        yield

    app = FastAPI(title="URL Shortener", lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
