from typing import TypedDict


class VolumeModel(TypedDict):
    block_number: int
    day: str
    game_chain: str
    game_id: str
    game_name: str
    id: str
    timestamp: int
    volume_token: float
    volume_transfers: int
    volume_usd: float
