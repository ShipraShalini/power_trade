from datetime import date, datetime
from enum import Enum

from tortoise import Model, fields


class TradeDirection(str, Enum):
    SELL = "sell"
    BUY = "buy"


class Trade(Model):
    id: str = fields.CharField(pk=True, max_length=255)
    price: int = fields.IntField()
    quantity: int = fields.IntField()
    direction: TradeDirection = fields.CharEnumField(TradeDirection)
    delivery_day: date = fields.DateField()
    delivery_hour: int = fields.IntField(min=0, max=23)
    trader_id: str = fields.CharField(max_length=255)
    execution_time: datetime = fields.DatetimeField()
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
