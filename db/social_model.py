from typing import Dict, List, TypedDict

class SocialModel(TypedDict):
    id: str
    game_id: str
    timestamp: int
    platform: str
    members: int
    channel_name: str
