from datetime import datetime
from pprint import pprint

from db.contract_aggregate_repo import ContractAggregateRepo
from db.game_repo import GameRepo
from dateutil import parser
from db.transaction_repo import TransactionRepo
from shared.get_midnight_utc import get_midnight_utc


class UserAnalyticsService:
    def __init__(
            self,
            game_repo: GameRepo,
    ):
        self.game_repo = game_repo

    def get_period_users(self, game, days):
        start = int(datetime.now().timestamp()) - days * 86400
        end = int(datetime.now().timestamp())

        eth_addresses = game['tokens']['eth']

        user_count_eth = 0

        return user_count_eth

    def get_last_period_chart(self, game, days):
        results = self.__get_chart(game, days * 2, days)

        if results is None:
            return None

        while (len(results) < (days - 1)):
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

        start = int(datetime.now().timestamp()) - start_days_ago * 86400
        end = int(datetime.now().timestamp()) - end_days_ago * 86400

        all_chain_results = []

        eth_addresses = game['tokens']['eth']

        if len(eth_addresses):
            results = []
            all_chain_results += results

        bsc_addresses = game['tokens']['bsc']

        if len(bsc_addresses):
            results = []
            all_chain_results += results

        if not len(all_chain_results):
            return None

        chart = {}

        for result in all_chain_results:
            dt = parser.parse(result['_id'])
            dtm = get_midnight_utc(dt)
            dtm_timestamp = dtm.timestamp()
            timestamp_ms = int(dtm_timestamp) * 1000
            active_users = result["active_users"]
            total_transfers = result["total_transfers"]

            chart_record = {
                "timestamp_ms": timestamp_ms,
                "active_users": active_users,
                "total_transfers": total_transfers
            }

            if str(timestamp_ms) in chart:
                chart_record = chart[str(timestamp_ms)]
                chart_record["active_users"] += active_users
                chart_record["total_transfers"] += total_transfers
            else:
                chart[str(timestamp_ms)] = chart_record

        result_list = list(
            sorted(
                chart.values(),
                key=lambda x: x['timestamp_ms']
            )
        )

        # pprint(result_list)

        return result_list
