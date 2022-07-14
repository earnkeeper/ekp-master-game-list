from typing import List, TypedDict

class AlertConfigModel(TypedDict):
    id: str
    created: int
    deleted: int
    discord_id: str
    latched: int
    min_volume: float
    new_users_above: float
    new_users_pc_above: float
    price_24h_pc_above: float
    public_address: str
    updated: int
