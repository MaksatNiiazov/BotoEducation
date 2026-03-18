from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any, Callable

_executor: ThreadPoolExecutor | None = None


def get_executor(max_workers: int = 8) -> ThreadPoolExecutor:
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="iss-worker")
    return _executor


async def run_sync(func: Callable[..., Any], *args: Any, max_workers: int = 8) -> Any:
    loop = asyncio.get_running_loop()
    executor = get_executor(max_workers=max_workers)
    return await loop.run_in_executor(executor, partial(func, *args))


def shutdown_executor() -> None:
    global _executor
    if _executor is not None:
        _executor.shutdown(wait=True, cancel_futures=True)
        _executor = None
