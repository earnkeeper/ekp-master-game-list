from ekp_sdk.db.mg_client import MgClient
import time
import logging

class ContractAggregateRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['contract_aggregates']

    def get_since(self, addresses, since):
        start = time.perf_counter()

        results = list(
            self.collection
            .aggregate([
                {
                    "$match": {
                        "contract_address": {"$in": addresses},
                        "timestamp": {"$gte": since}
                    }
                },
                {"$sort": {"timestamp": 1}},
                {
                    "$group":
                    {
                        "_id": "$timestamp",
                        "active_users": {"$sum": "$active_users"},
                        "total_transfers": {"$sum": "$total_transfers"},
                    }
                }
            ])
        )

        logging.info(
            f"⏱  [ContractAggregateRepo.get_since({addresses}, {since})] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return []

        return results
