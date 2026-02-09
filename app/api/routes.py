from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.core.config import get_settings
from app.models.shorten import ShortenRequest, ShortenResponse
from app.services import shortener

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(payload: ShortenRequest) -> ShortenResponse:
    settings = get_settings()
    try:
        code = shortener.create_short_code(payload.url)
    except shortener.InvalidUrlError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except shortener.StorageError as exc:
        logger.exception("Failed to create short URL.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error") from exc

    base_url = settings.base_url.rstrip("/")
    return ShortenResponse(short_url=f"{base_url}/{code}")


@router.get(
    "/{code}",
    status_code=status.HTTP_302_FOUND,
    response_class=RedirectResponse,
    responses={
        302: {"description": "Redirect"},
        404: {"description": "Short code not found"},
        500: {"description": "Internal error"},
    },
)
def redirect_to_original(code: str) -> RedirectResponse:
    try:
        url = shortener.get_original_url(code)
    except shortener.NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except shortener.StorageError as exc:
        logger.exception("Failed to redirect.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error") from exc

    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
