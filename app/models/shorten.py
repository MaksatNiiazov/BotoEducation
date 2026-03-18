from __future__ import annotations

from pydantic import AnyHttpUrl, BaseModel


class ShortenRequest(BaseModel):
    url: AnyHttpUrl


class ShortenResponse(BaseModel):
    short_url: str


class LinkInfo(BaseModel):
    code: str
    url: str
    created_at: str
