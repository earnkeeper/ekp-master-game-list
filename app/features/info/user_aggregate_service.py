from datetime import datetime

from db.contract_aggregate_repo import ContractAggregateRepo
from db.game_repo import GameRepo
from shared.get_midnight_utc import get_midnight_utc
from db.activity_repo import ActivityRepo


class UserAggregateService:
    def __init__(
            self,
            contract_aggregate_repo: ContractAggregateRepo,
            game_repo: GameRepo,
    ):
        self.contract_aggregate_repo = contract_aggregate_repo
        self.game_repo = game_repo

    async def get_user_aggregate_document(self, game):
        # game = self.game_repo.find_one_by_id(game["id"])

        eth_addresses = game['tokens']['eth']

        if not len(eth_addresses):
            return None

        results = self.contract_aggregate_repo.get_since(eth_addresses, 0)

        return results



        # if len(eth_addresses):
        #     results = self.contract_aggregate_repo.get_since(eth_addresses, 0)
        #     print(len(results))

