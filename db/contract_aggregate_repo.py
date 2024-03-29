import pytz
from dateutil import parser
from ekp_sdk.db.mg_client import MgClient
import time as t
import logging
from datetime import datetime, time, date


class ContractAggregateRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['contract_aggregates']

    def get_users_activity_of_all_games_by_timestamp(self, start_timestamp, end_timestamp):
        results = list(self.collection.aggregate([
            {
                "$match": {
                    "timestamp": {
                        "$gte": start_timestamp,
                        "$lt": end_timestamp
                    }
                }
            },
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
                        # "_id": "$timestamp",
                        "total_active_users": {"$sum": "$active_users"},
                        "total_total_transfers": {"$sum": "$total_transfers"}

                    }

            },
            {
                "$project": {
                    "_id": 0,
                    "timestamp": "$_id",
                    "active_users": "$total_active_users",
                    "total_transfers": "$total_total_transfers",
                }
            }
        ]
        ))

        if not len(results):
            return []

        return results

    def get_range(self, addresses, start_timestamp, end_timestamp):
        start = t.perf_counter()

        results = self.collection.aggregate([
            {
                "$match": {
                    "contract_address": {"$in": addresses},
                    "timestamp": {
                        "$gte": start_timestamp,
                        "$lt": end_timestamp
                    }
                }
            },
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
            f"⏱  [ContractAggregateRepo.get_since({addresses})] {t.perf_counter() - start:0.3f}s"
        )

        return results
