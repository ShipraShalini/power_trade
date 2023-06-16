import json
from pathlib import Path

import pytest
from httpx import AsyncClient

from power.models import Trade


@pytest.mark.parametrize(
    "query_params, expected_trade_ids",
    [
        (
            {},
            [
                "t_123",
                "t_456",
                "t_337",
                "t_789",
                "t_160",
                "t_320",
                "t_353",
                "t_962",
                "t_468",
                "t_188",
                "t_357",
                "t_585",
                "t_215",
            ],
        ),
        ({"trader_id": "trader_2"}, ["t_456", "t_789"]),
        ({"delivery_day": "2023-06-14"}, ["t_123", "t_456"]),
        ({"trader_id": "trader_2", "delivery_day": "2023-06-14"}, ["t_456"]),
    ],
)
@pytest.mark.asyncio
async def test_get_trades(
    client: AsyncClient, fixtures_path: Path, sample_trades: list[Trade], query_params: dict, expected_trade_ids: list
):
    # Arrange
    sample_trades = json.loads((fixtures_path / "sample_trades.json").read_text())
    expected_trades = [trade for trade in sample_trades if trade["id"] in expected_trade_ids]

    # Act
    response = await client.get("/trades", params=query_params)

    # Assert
    assert response.status_code == 200

    response_data = response.json()
    assert response_data == expected_trades


@pytest.mark.asyncio
async def test_post_trade(client: AsyncClient, fixtures_path: Path):
    # Arrange
    trade_data = {
        "id": "trade124",
        "price": 2314,
        "quantity": 12,
        "direction": "sell",
        "delivery_day": "2023-06-15",
        "delivery_hour": 12,
        "trader_id": "Shipra",
        "execution_time": "2023-06-15 10:34:38.480000Z",
    }

    # Act
    response = await client.post("/trades", json=trade_data)

    # Assert
    assert response.status_code == 200

    trade = await Trade.get(id=trade_data["id"])

    for field, expected_value in trade_data.items():
        value = getattr(trade, field, None)
        if field in ["delivery_day", "execution_time"]:
            value = str(value).replace("+00:00", "Z")
        assert value == expected_value
