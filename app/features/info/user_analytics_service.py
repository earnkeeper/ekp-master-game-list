from datetime import datetime

from db.contract_aggregate_repo import ContractAggregateRepo
from db.game_repo import GameRepo
from dateutil import parser
from shared.get_midnight_utc import get_midnight_utc


class UserAnalyticsService:
    def __init__(
            self,
            contract_aggregate_repo: ContractAggregateRepo,
            game_repo: GameRepo,
    ):
        self.contract_aggregate_repo = contract_aggregate_repo
        self.game_repo = game_repo

    def get_last_period_chart(self, game, days):
        results = self.__get_chart(game, days * 2, days)
        while (len(results) < (days -1)):
            results.insert(
                0,
                {
                    "timestamp_ms": 0,
                    "active_users": None,
                    "total_transfers": None
                }
            )
        return results

    def get_period_chart(self, game, days):
        return self.__get_chart(game, days, 0)

    def __get_chart(self, game, start_days_ago, end_days_ago):

        eth_addresses = game['tokens']['eth']

        if not len(eth_addresses):
            return []

        start = int(datetime.now().timestamp()) - start_days_ago * 86400
        end = int(datetime.now().timestamp()) - end_days_ago * 86400

        results = self.contract_aggregate_repo.get_range(
            eth_addresses,
            start,
            end
        )

        chart = []

        for result in results:
            chart_record = {}
            dt = parser.parse(result['_id'])
            dtm = get_midnight_utc(dt)
            dtm_timestamp = dtm.timestamp()
            chart_record["timestamp_ms"] = int(dtm_timestamp) * 1000
            chart_record["active_users"] = result["active_users"]
            chart_record["total_transfers"] = result["total_transfers"]
            chart.append(chart_record)

        return chart
