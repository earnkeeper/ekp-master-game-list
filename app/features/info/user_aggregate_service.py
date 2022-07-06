from datetime import datetime

from db.contract_aggregate_repo import ContractAggregateRepo
from db.game_repo import GameRepo
from shared.get_midnight_utc import get_midnight_utc
from db.activity_repo import ActivityRepo


def labels_to_values(argument):
    switcher = {
        "Last 7 days": 7,
        "Last 28 days": 28,
        "Last 3 months": 92,
        "Last 12 months": 365,
        "all": "all"
    }

    return switcher.get(argument, "all")


class UserAggregateService:
    def __init__(
            self,
            contract_aggregate_repo: ContractAggregateRepo,
            game_repo: GameRepo,
    ):
        self.contract_aggregate_repo = contract_aggregate_repo
        self.game_repo = game_repo

    async def get_user_aggregate_document(self, game, aggregate_days_form_value):
        # game = self.game_repo.find_one_by_id(game["id"])

        eth_addresses = game['tokens']['eth']

        if not len(eth_addresses):
            return None

        days_input = labels_to_values(aggregate_days_form_value)

        results = self.contract_aggregate_repo.get_since(eth_addresses, 0, days_input)

        return results

        # if len(eth_addresses):
        #     results = self.contract_aggregate_repo.get_since(eth_addresses, 0)
        #     print(len(results))
