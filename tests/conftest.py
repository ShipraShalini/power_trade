import asyncio
import json
from asyncio import AbstractEventLoop
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import AsyncClient
from tortoise import current_transaction_map
from tortoise.contrib import test as tortoise_test

from main import app
from power.constants import PROJECT_DIR
from power.models import Trade
from power.settings import DB_MODULES


@pytest.fixture(scope="module", autouse=True)
def initialize_tests(request):
    # The {} allows tortoise test to append a random string at the end.
    tortoise_test.initializer(modules=DB_MODULES["models"], app_label="models")
    current_transaction_map["default"] = current_transaction_map["models"]
    request.addfinalizer(tortoise_test.finalizer)


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def fixtures_path() -> Path:
    return PROJECT_DIR / "tests" / "fixtures"


@pytest_asyncio.fixture(scope="module")
async def sample_trades(fixtures_path) -> list[Trade]:
    trades = json.loads((fixtures_path / "sample_trades.json").read_text())
    return await Trade.bulk_create(Trade(**trade) for trade in trades)
