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

    def get_last_period_chart(self, game, days):
        return self.__get_chart(game, days * 2, days)

    def get_period_chart(self, game, days):
        return self.__get_chart(game, days, 0)

    def __get_chart(self, game, start_days_ago, end_days_ago):
        eth_addresses = game['tokens']['eth']

        if not len(eth_addresses):
            return None

        start = int(datetime.now().timestamp()) - start_days_ago * 86400
        end = int(datetime.now().timestamp()) - end_days_ago * 86400

        results = self.contract_aggregate_repo.get_range(
            eth_addresses,
            start,
            end
        )

        return results
