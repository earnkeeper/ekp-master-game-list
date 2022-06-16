from typing import TypedDict


class PriceModel(TypedDict):
    game_id: str
    game_name: str
    id: str
    timestamp: int
    price_usd: float
