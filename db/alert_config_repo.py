from ekp_sdk.db import MgClient
import logging
import time
from pymongo import UpdateOne


class AlertConfigRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['alert_config']

    def get_all_alert_configs(self):
        results = list(self.collection.find().sort("created", -1))

        if not len(results):
            return []

        return results

    def save(self, models):

        if not len(models):
            return

        start = time.perf_counter()

        def update_action(model):
            new_model = model
            if "_id" in new_model:
                del new_model["_id"]
            return UpdateOne({"id": model["id"]}, {"$set": model}, True)

        self.collection.bulk_write(
            list(map(lambda model: update_action(model), models))
        )

        logging.info(f"⏱  [AlertConfigRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s")
