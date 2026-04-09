from pydantic import BaseModel
from typing import List


class Order(BaseModel):
    symbol: str
    quantity: int
    action: str   # BUY / SELL


class TradeRequest(BaseModel):
    code: str
    broker: str
    orders: List[Order]


class TradeResult(BaseModel):
    symbol: str
    status: str
    message: str