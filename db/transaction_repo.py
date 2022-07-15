from ekp_sdk.db.mg_client import MgClient
import time as t
import logging


class TransactionRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['transactions']

    def get_active_user_count(self, addresses, start_timestamp, end_timestamp):
        start = t.perf_counter()

        count = len(list(self.collection.distinct(
            "from",
            {
                "to": {"$in": addresses},
                "timestamp": {
                    "$gte": start_timestamp,
                    "$lt": end_timestamp
                }
            }
        )))

        logging.info(
            f"⏱  [TransactionRepo.get_active_user_count({addresses})] {t.perf_counter() - start:0.3f}s"
        )

        return count
