from datetime import datetime
from db.game_repo import GameRepo
from db.shared_games_repo import SharedGamesRepo
from db.transaction_repo import TransactionRepo


class SharedGamesService:

    def __init__(
            self,
            shared_games_repo: SharedGamesRepo
            # transaction_repo: TransactionRepo,
            # game_repo: GameRepo,
    ):
        # self.transaction_repo = transaction_repo
        # self.game_repo = game_repo
        self.shared_games_repo = shared_games_repo

    def get_games(self, game):
        # game_contracts = game['tokens']['bsc']

        shared_games = self.shared_games_repo.find_shared_games_by_game_id(game['id'])

        return shared_games
