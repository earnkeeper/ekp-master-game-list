from typing import TypedDict


class VolumeModel(TypedDict):
    game_id: str
    game_name: str
    id: str
    timestamp: int
    volume_usd: float
