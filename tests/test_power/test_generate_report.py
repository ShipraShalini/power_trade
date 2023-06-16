from datetime import date

import pytest
from freezegun import freeze_time

from generate_report_script import generate_trade_report
from power.models import Trade


@pytest.mark.asyncio
async def test_generate_trade_report(sample_trades: list[Trade]):
    # Arrange
    expected_result = [
        {"hour": 7, "number_of_trades": 1, "total_buy": 0, "total_sell": 307, "pnl": 9824},
        {"hour": 8, "number_of_trades": 3, "total_buy": 102, "total_sell": 734, "pnl": 47361},
        {"hour": 9, "number_of_trades": 1, "total_buy": 0, "total_sell": 51, "pnl": 4845},
        {"hour": 13, "number_of_trades": 1, "total_buy": 75, "total_sell": 0, "pnl": -50925},
    ]

    # Act
    result_specific_date = await generate_trade_report(
        trader_id="trader_23", delivery_day=date.fromisoformat("2023-06-13")
    )

    with freeze_time("2023-06-13"):
        result_today = await generate_trade_report(trader_id="trader_23")

    assert expected_result == result_specific_date == result_today
