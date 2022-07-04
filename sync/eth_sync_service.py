import logging

from db.game_repo_eth import GameRepoEth
from db.game_repo import GameRepo


class EthSyncService:
    def __init__(
        self,
        game_repo: GameRepo,
        game_repo_eth: GameRepoEth
    ):
        self.game_repo = game_repo
        self.eth_games_repo = game_repo_eth

    async def sync_games(self):
        eth_games = list(self.game_repo.collection.find({
            "tokens.eth": {
                "$ne": []
            }
        }))

        self.eth_games_repo.save(eth_games)




