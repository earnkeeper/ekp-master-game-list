from typing import TypedDict


class ActivityModel(TypedDict):
    block_number: int
    day: str
    game_name: str
    game_id: str
    game_chain: str
    id: str
    new_users: int
    timestamp: int
    transactions: int
