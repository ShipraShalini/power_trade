from collections import defaultdict
from datetime import date
from typing import Optional

from power.models import Trade, TradeDirection


async def generate_trade_report(trader_id: str, delivery_day: Optional[date] = None):
    trades = await Trade.filter(trader_id=trader_id, delivery_day=delivery_day or date.today()).order_by(
        "delivery_hour"
    )
    trades_by_hour = defaultdict(list)

    for trade in trades:
        trades_by_hour[trade.delivery_hour].append(trade)

    report = []
    for hour, trades in trades_by_hour.items():
        total_buy = 0
        total_sell = 0
        pnl = 0
        for trade in trades:
            if trade.direction == TradeDirection.BUY.value:
                total_buy += trade.quantity
                pnl -= trade.quantity * trade.price
            else:
                total_sell += trade.quantity
                pnl += trade.quantity * trade.price
        report.append(
            {
                "hour": hour,
                "number_of_trades": len(trades),
                "total_buy": total_buy,
                "total_sell": total_sell,
                "pnl": pnl,
            }
        )

    return report
