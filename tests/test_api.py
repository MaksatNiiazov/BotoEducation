from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("APP_HOST", "127.0.0.1")
    monkeypatch.setenv("APP_PORT", "8000")
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    monkeypatch.setenv("BASE_URL", "http://testserver")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    get_settings.cache_clear()

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_shorten_and_redirect(client: TestClient) -> None:
    response = client.post("/shorten", json={"url": "https://example.com/long"})
    assert response.status_code == 201
    short_url = response.json()["short_url"]
    assert short_url.startswith("http://testserver/")

    code = short_url.rsplit("/", 1)[-1]
    redirect_response = client.get(f"/{code}", follow_redirects=False)
    assert redirect_response.status_code == 302
    assert redirect_response.headers["location"] == "https://example.com/long"


def test_shorten_invalid_url(client: TestClient) -> None:
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 400


def test_redirect_missing_code(client: TestClient) -> None:
    response = client.get("/missing", follow_redirects=False)
    assert response.status_code == 404
