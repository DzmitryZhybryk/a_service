from typing import AsyncGenerator

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def prefix() -> str:
    """Fixture create URL prefix"""
    return "/api/v1/"


@pytest.fixture
async def index_page(prefix: str, test_client: TestClient) -> AsyncGenerator[httpx.Response, None]:
    """Fixture make index page response"""
    response = test_client.get(prefix)
    yield response
