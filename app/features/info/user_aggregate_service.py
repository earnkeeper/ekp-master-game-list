from datetime import datetime

from db.contract_aggregate_repo import ContractAggregateRepo
from db.game_repo import GameRepo


def labels_to_values(argument):
    switcher = {
        "Last 7 days": 7,
        "Last 28 days": 28,
        "Last 3 months": 92,
        "Last 12 months": 365,
    }

    return switcher.get(argument, 365)


class UserAggregateService:
    def __init__(
            self,
            contract_aggregate_repo: ContractAggregateRepo,
            game_repo: GameRepo,
    ):
        self.contract_aggregate_repo = contract_aggregate_repo
        self.game_repo = game_repo

    def get_last_period_chart(self, game, aggregate_days_form_value):
        days = labels_to_values(aggregate_days_form_value)
        return self.__get_chart(game, days * 2, days)

    def get_period_chart(self, game, aggregate_days_form_value):
        days = labels_to_values(aggregate_days_form_value)        
        return self.__get_chart(game, days, 0)

    def __get_chart(self, game, start_days_ago, end_days_ago):
        
        print(start_days_ago)
        print(end_days_ago)
        
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
