from typing import TypedDict


class RoadmapEventModel(TypedDict):
    description: str
    event: str
    game_id: str
    month: int
    phase: str
    quarter: int
    timestamp: int
    updated: int
    year: int