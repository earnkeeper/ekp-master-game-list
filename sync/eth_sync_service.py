import logging

from db.eth_games_repo import EthGamesRepo
from db.game_repo import GameRepo


class EthSyncService:
    def __init__(
        self,
        game_repo: GameRepo,
        eth_games_repo: EthGamesRepo
    ):
        self.game_repo = game_repo
        self.eth_games_repo = eth_games_repo

    async def sync_games(self):
        eth_games = list(self.game_repo.collection.find({
            "tokens.eth": {
                "$ne": []
            }
        }))

        self.eth_games_repo.save(eth_games)




