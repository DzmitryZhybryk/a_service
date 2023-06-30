from typing import AsyncGenerator

import httpx
import pytest
import pytest_check as check
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

test_client = TestClient(app)


@pytest.mark.integration
@pytest.mark.asyncio
class TestIndex:

    async def test_index_response_status(self, index_page: AsyncGenerator[httpx.Response, None]):
        async for response in index_page:
            assert response.status_code == status.HTTP_200_OK

    async def test_index_response_json(self, index_page: AsyncGenerator[httpx.Response, None]):
        async for response in index_page:
            response_json = response.json()
            check.is_not_none(response_json.get("name"))
            check.is_not_none(response_json.get("version"))
            check.is_not_none(response_json.get("description"))
            check.is_not_none(response_json.get("environment"))
            check.is_not_none(response_json.get("run_mode"))
            check.is_not_none(response_json.get("logs_dir"))

    async def test_index_expect_403(self, index_page: AsyncGenerator[httpx.Response, None]):
        async for response in index_page:
            assert response.status_code == status.HTTP_403_FORBIDDEN
