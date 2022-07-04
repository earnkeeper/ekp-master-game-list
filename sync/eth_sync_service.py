from db.game_repo import GameRepo


class EthSyncService:
    def __init__(
        self,
        game_repo: GameRepo,
        game_repo_eth: GameRepo
    ):
        self.game_repo = game_repo
        self.game_repo_eth = game_repo_eth

    async def sync_games(self):
        games_eth = list(
            self.game_repo.collection.find(
                {
                    "tokens.eth": {
                        "$ne": []
                    }
                }
            )
        )

        self.game_repo_eth.save(games_eth)
