from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import RedirectResponse

from app.core.config import get_settings
from app.core.executor import run_sync
from app.core.security import parse_user_token
from app.models.shorten import LinkInfo, ShortenRequest, ShortenResponse
from app.services import shortener

router = APIRouter()


def _extract_user_id(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    try:
        return parse_user_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


@router.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(payload: ShortenRequest, authorization: str | None = Header(default=None)) -> ShortenResponse:
    settings = get_settings()
    user_id = _extract_user_id(authorization)
    try:
        code = await run_sync(
            shortener.create_short_code,
            user_id,
            str(payload.url),
            max_workers=settings.thread_pool_workers,
        )
    except shortener.StorageError as exc:
        raise HTTPException(status_code=500, detail="Internal error") from exc
    return ShortenResponse(short_url=f"{settings.base_url.rstrip('/')}/{code}")


@router.get("/{code}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def redirect_to_original(code: str) -> RedirectResponse:
    settings = get_settings()
    try:
        url = await run_sync(shortener.get_original_url, code, max_workers=settings.thread_pool_workers)
    except shortener.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except shortener.StorageError as exc:
        raise HTTPException(status_code=500, detail="Internal error") from exc
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/me/links", response_model=list[LinkInfo])
async def my_links(authorization: str | None = Header(default=None)) -> list[LinkInfo]:
    settings = get_settings()
    user_id = _extract_user_id(authorization)
    rows = await run_sync(shortener.get_user_links, user_id, max_workers=settings.thread_pool_workers)
    return [LinkInfo(**row) for row in rows]
