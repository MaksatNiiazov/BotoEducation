from __future__ import annotations

import asyncio
import os

import uvicorn

from app.bot.runner import run_bot
from app.main import app


async def _run() -> None:
    config = uvicorn.Config(
        app,
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "8000")),
        log_level="info",
    )
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())
    bot_task = asyncio.create_task(run_bot())
    await asyncio.gather(api_task, bot_task)


if __name__ == "__main__":
    asyncio.run(_run())
