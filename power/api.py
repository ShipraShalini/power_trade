from datetime import date
from typing import Optional

from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from tortoise.exceptions import IntegrityError

from power.models import Trade
from power.schemas import Trade_Pydantic

router = APIRouter(prefix="/trades")


@router.get("", response_model=list[Trade_Pydantic])
async def get_trades(trader_id: Optional[str] = None, delivery_day: Optional[date] = None):
    """Get trades from the database.

    Trades can be filtered based on `trader_id` and/or `delivery_day`.
    """
    filter_kwargs = {}
    if trader_id:
        filter_kwargs["trader_id"] = trader_id
    if delivery_day:
        filter_kwargs["delivery_day"] = delivery_day
    return await Trade.filter(**filter_kwargs).order_by("-execution_time")


@router.post("")
async def post_trades(trade: Trade_Pydantic):
    """Add new trade to the database."""
    # ToDo: Check why Pydantic is not validating TradeDirection & datetime.
    try:
        await Trade.create(**trade.dict())
    except IntegrityError as e:
        raise RequestValidationError(errors=[ErrorWrapper(exc=e, loc=("body", "id"))]) from e
