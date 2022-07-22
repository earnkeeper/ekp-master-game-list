import logging
from db.game_repo import GameRepo


class RemoteSyncService:
    def __init__(
        self,
        game_repo: GameRepo,
        game_repo_eth: GameRepo,
        game_repo_bsc: GameRepo,
    ):
        self.game_repo = game_repo
        self.game_repo_eth = game_repo_eth
        self.game_repo_bsc = game_repo_bsc

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

        logging.info(f"Saved {len(games_eth)} games to eth node")

        games_bsc = list(
            self.game_repo.collection.find(
                {
                    "tokens.bsc": {
                        "$ne": []
                    }
                }
            )
        )
        
        self.game_repo_bsc.save(games_bsc)
        
        logging.info(f"Saved {len(games_bsc)} games to bsc node")
