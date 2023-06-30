from functools import lru_cache
from pathlib import Path
from typing import AsyncGenerator

import httpx
import pytest
import yaml
from fastapi.testclient import TestClient
from pytest import Metafunc

from app.config import config
from app.database.models import Role, User
from app.database.postgres import engine, Base
from app.main import app

CURRENT_DIR = Path(__file__).parent


@lru_cache
def read_json_file() -> dict:
    with open(f"{CURRENT_DIR}/test_data.yaml", "r") as file:
        try:
            test_data = yaml.safe_load(file)
            return test_data
        except yaml.YAMLError as err:
            pass


def pytest_generate_tests(metafunc) -> Metafunc:
    all_params = read_json_file()
    fct_name = metafunc.function.__name__
    if fct_name in all_params:
        func_params = all_params[fct_name]
        return metafunc.parametrize(func_params["params"], func_params["values"])


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def base_headers():
    headers = {"X-API_Key": config.secret.secret_key}
    return headers


@pytest.fixture
async def database_init_fixture() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    role, user = Role(), User()
    await role.create_init_roles()
    await user.creat_init_user()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def index_page(test_client: TestClient,
                     base_headers: dict,
                     rout_url: str,
                     use_api_key: bool) -> AsyncGenerator[httpx.Response, None]:
    """Fixture make index page response"""
    yield test_client.get(url=rout_url, headers=base_headers) if use_api_key else test_client.get(url=rout_url)


@pytest.fixture
async def registrate_page(database_init_fixture: AsyncGenerator[None, None],
                          test_client: TestClient,
                          base_headers: dict,
                          rout_url: str,
                          test_user: dict,
                          use_api_key: bool) -> AsyncGenerator[httpx.Response, None]:
    """Fixture make registrate page response"""
    async for _ in database_init_fixture:
        yield test_client.post(url=rout_url, headers=base_headers, json=test_user) if use_api_key \
            else test_client.post(url=rout_url, json=test_user)
