from datetime import datetime
from pprint import pprint

from db.contract_aggregate_repo import ContractAggregateRepo
from db.game_repo import GameRepo
from dateutil import parser
from db.transaction_repo import TransactionRepo
from shared.get_midnight_utc import get_midnight_utc


class AllUsersAnalyticsService:
    def __init__(
            self,
            contract_aggregate_repo_eth: ContractAggregateRepo,
            contract_aggregate_repo_bsc: ContractAggregateRepo,
            transaction_repo_eth: TransactionRepo,
            game_repo: GameRepo,
    ):
        self.contract_aggregate_repo_eth = contract_aggregate_repo_eth
        self.contract_aggregate_repo_bsc = contract_aggregate_repo_bsc
        self.transaction_repo_eth = transaction_repo_eth
        self.game_repo = game_repo


    def get_last_period_chart(self, days):
        results = self.__get_chart(days * 2, days)

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

    def get_period_chart(self, days):
        return self.__get_chart(
            # game,
            days,
            0)

    def __get_chart(
            self,
            # game,
            start_days_ago,
            end_days_ago):

        start = int(datetime.now().timestamp()) - start_days_ago * 86400
        end = int(datetime.now().timestamp()) - end_days_ago * 86400

        # print(start)
        # print(end)

        bsc_results = self.contract_aggregate_repo_bsc.get_users_activity_of_all_games_by_timestamp(
            start_timestamp=start,
            end_timestamp=end
        )

        # pprint('bsc_results: ')
        # pprint(bsc_results)

        eth_results = self.contract_aggregate_repo_eth.get_users_activity_of_all_games_by_timestamp(
            start_timestamp=start,
            end_timestamp=end
        )

        # pprint('eth_results: ')
        # pprint(eth_results)

        timestamps = set([k['timestamp'] for k in bsc_results + eth_results])
        all_chain_results = []
        for timestamp in timestamps:
            temp_active_users = []
            temp_total_transfers = []
            for dict_ in bsc_results + eth_results:
                if dict_['timestamp'] == timestamp:
                    temp_active_users.append(dict_['active_users'])
                    temp_total_transfers.append(dict_['total_transfers'])
            all_chain_results.append({'timestamp': timestamp,
                          'active_users': sum(temp_active_users),
                          'total_transfers': sum(temp_total_transfers),
                          })

        # pprint(dict3)
        # return []
        chart = {}

        for result in all_chain_results:
            dt = parser.parse(result['timestamp'])
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

        return result_list
