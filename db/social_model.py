from typing import Dict, List, TypedDict

class SocialModel(TypedDict):
    id: str
    game_id: str
    timestamp: int
    twitter_followers: int
    telegram_members: int
