from typing import List, TypedDict

class GamePlatformTokens(TypedDict):
    bsc: List[str]
    eth: List[str]
    polygon: List[str]

class GameModel(TypedDict):
    id: str
    name: str
    tokens: GamePlatformTokens
    twitter: str
    telegram: str
    website: str
    discord: str
    coin_ids: List[str]
