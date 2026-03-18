from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import get_settings


def create_user_token(user_id: str, minutes: int = 60) -> str:
    s = get_settings()
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_algorithm)


def parse_user_token(token: str) -> str:
    s = get_settings()
    payload = jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_algorithm])
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Token has no sub")
    return str(user_id)
