from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, StrictInt

from power.models import TradeDirection


class Trade_Pydantic(BaseModel):
    id: str
    price: StrictInt = Field(min=1)
    quantity: StrictInt = Field(min=1)
    direction: TradeDirection
    delivery_day: date
    delivery_hour: StrictInt = Field(max=23)
    trader_id: str
    execution_time: datetime
    created_at: Optional[datetime] = Field(exclude=True)

    class Config:
        max_anystr_length = 255
        min_anystr_length = 1
        extra = Extra.forbid
        json_encoders = {
            datetime: lambda v: v.isoformat().replace("+00:00", "Z"),
        }
