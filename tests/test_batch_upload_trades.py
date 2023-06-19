from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
import requests
from _pytest.capture import CaptureFixture
from freezegun import freeze_time

from batch_upload_trades import add_new_trades, main


@pytest.mark.asyncio
@freeze_time("2023-06-15")
@patch.object(requests, "get")
@patch.object(requests, "post")
async def test_main(
    patched_requests_post: MagicMock,
    patched_requests_get: MagicMock,
    fixtures_path: Path,
):
    # Arrange
    TRADE_URL = "http://localhost:8000/trades"
    patched_requests_get.return_value.status_code = 200
    patched_requests_get.return_value.json.return_value = [
        {"id": "t_123"},
        {"id": "t_456"},
    ]

    expected_calls = [
        call(
            TRADE_URL,
            json={
                "id": "t_653",
                "price": "120",
                "quantity": "12",
                "direction": "sell",
                "delivery_day": "2023-06-14",
                "delivery_hour": "14",
                "trader_id": "trader_1",
                "execution_time": "2023-06-14T11:12:35Z",
            },
            timeout=30,
        ),
        call(
            TRADE_URL,
            json={
                "id": "t_776",
                "price": "78",
                "quantity": "57",
                "direction": "buy",
                "delivery_day": "2023-06-14",
                "delivery_hour": "9",
                "trader_id": "trader_2",
                "execution_time": "2023-06-14T07:45:12Z",
            },
            timeout=30,
        ),
        call(
            TRADE_URL,
            json={
                "id": "t_874",
                "price": "34",
                "quantity": "18",
                "direction": "sell",
                "delivery_day": "2023-06-14",
                "delivery_hour": "20",
                "trader_id": "trader_2",
                "execution_time": "2023-06-14T16:23:38Z",
            },
            timeout=30,
        ),
    ]

    # Act
    with patch("batch_upload_trades.CSV_DIR", fixtures_path.as_posix()):
        main()

    # Assert
    patched_requests_get.assert_called_once_with(TRADE_URL, params={"delivery_day": "2023-06-14"}, timeout=30)

    patched_requests_post.assert_has_calls(expected_calls, any_order=True)


@pytest.mark.asyncio
@patch.object(requests, "post")
async def test_add_new_trades_filenotfound(
    patched_requests_post: MagicMock, fixtures_path: Path, capsys: CaptureFixture
):
    # Arrange
    existing_trade_ids = ["t_123", "t_456"]
    delivery_day = date.fromisoformat("2023-06-18")

    with patch("batch_upload_trades.CSV_DIR", fixtures_path.as_posix()):
        with pytest.raises(SystemExit):
            add_new_trades(existing_trade_ids, delivery_day)

    assert capsys.readouterr().err == f"File epex_trades_20230618.csv not found at {fixtures_path.as_posix()}\n"
    patched_requests_post.assert_not_called()
