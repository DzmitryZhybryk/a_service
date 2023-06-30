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
class TestRegistrate:

    async def test_registrate_response_status(self, registrate_page: AsyncGenerator[httpx.Response, None]):
        async for response in registrate_page:
            assert response.status_code == status.HTTP_201_CREATED

    async def test_registrate_user(self, registrate_page: AsyncGenerator[httpx.Response, None]):
        async for response in registrate_page:
            response_json = response.json()
            check.is_not_none(response_json.get("confirm_registration_key"))
            check.is_not_none(response_json.get("username"))
            check.is_not_none(response_json.get("email"))

    async def test_registrate_user_expect_422(self, registrate_page: AsyncGenerator[httpx.Response, None]):
        async for response in registrate_page:
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_registrate_user_expect_409(self, registrate_page: AsyncGenerator[httpx.Response, None]):
        async for response in registrate_page:
            assert response.status_code == status.HTTP_409_CONFLICT

    async def test_registrate_user_expected_403(self, registrate_page: AsyncGenerator[httpx.Response, None]):
        async for response in registrate_page:
            assert response.status_code == status.HTTP_403_FORBIDDEN
