from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.executor import shutdown_executor
from app.core.logging import configure_logging
from app.db.database import init_db


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        s = get_settings()
        configure_logging(s.log_level, s.log_file_path)
        init_db()
        try:
            yield
        finally:
            shutdown_executor()

    app = FastAPI(title="ISS Shortener", lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
