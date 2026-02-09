from __future__ import annotations

from pydantic import BaseModel


class ShortenRequest(BaseModel):
    url: str


class ShortenResponse(BaseModel):
    short_url: str
