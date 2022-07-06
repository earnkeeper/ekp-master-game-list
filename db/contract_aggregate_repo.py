import pytz
from dateutil import parser
from ekp_sdk.db.mg_client import MgClient
import time as t
import logging
from datetime import datetime, time, date


def get_midnight_utc(dt=None):
    if dt is None:
        dt = datetime.now()

    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    dt = pytz.utc.localize(dt)

    return dt


class ContractAggregateRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['contract_aggregates']

    def get_since(self, addresses, since):
        start = t.perf_counter()

        results = self.collection.aggregate([
            {
                "$match": {
                    "contract_address": {"$in": addresses},
                    "timestamp": {"$gte": since}
                }
            },
            # {"$sort": {"timestamp": 1}},
            {
                "$group":
                    {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": {
                                    "$convert": {
                                        "input": {
                                            "$multiply": [1000, "$timestamp"]
                                        },
                                        "to": "date"
                                    }
                                }
                            }
                        },
                        "active_users": {"$sum": "$active_users"},
                        "total_transfers": {"$sum": "$total_transfers"},
                    }
            }
        ])

        results = sorted(results, key=lambda x: x['_id'], reverse=True)

        logging.info(
            f"⏱  [ContractAggregateRepo.get_since({addresses}, {since})] {t.perf_counter() - start:0.3f}s"
        )

        new_result_list = []

        total_transfers = 0
        active_users = 0
        for result in results:
            new_result_dict = {}
            dt = parser.parse(result['_id'])
            dtm = get_midnight_utc(dt)
            dtm_timestamp = dtm.timestamp()
            total_transfers += result["total_transfers"]
            active_users += result["active_users"]
            new_result_dict["timestamp_ms"] = int(dtm_timestamp) * 1000
            new_result_dict["active_users"] = result["active_users"]
            new_result_dict["total_transfers"] = result["total_transfers"]
            new_result_list.append(new_result_dict)

        final_documents = {
            "active_users_sum": active_users,
            "total_transfers_sum": total_transfers,
            "chart": new_result_list
        }

        return final_documents
