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
            print("############")
            print(response.json())
            # assert response.status_code == status.HTTP_200_OK
