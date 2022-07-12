import logging
from ekp_sdk.db import MgClient
from pymongo import UpdateOne
import time


class PriceRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['token_price']
        self.collection.create_index("id", unique=True)
        self.collection.create_index("timestamp")
        self.collection.create_index("game_id")
        self.collection.create_index("block_number")
        self.collection.create_index("latest")

    def find_all(self):
        return list(
            self.collection.find().sort("timestamp")
        )

    def find_latest_price_by_game_id(self):

        results = list(
            self.collection.aggregate([
                {"$match": {"latest": True}},
                {"$sort": {"timestamp": 1}},
                {
                    "$group":
                    {
                        "_id": "$game_id",
                        "price": {"$last": "$price_usd"},
                        "timestamp": {"$last": "$timestamp"},
                    }
                }
            ])
        )

        if not len(results):
            return []

        return results

    def find_latest_daily_price_by_game_id(self):

        results = list(
            self.collection.aggregate([
                {"$match": {"latest": False}},
                {"$sort": {"timestamp": 1}},
                {
                    "$group":
                    {
                        "_id": "$game_id",
                        "price": {"$last": "$price_usd"},
                        "timestamp": {"$last": "$timestamp"},
                    }
                }
            ])
        )

        if not len(results):
            return []

        return results

    def find_by_game_id(self, game_id):
        return list(self.collection.find({"game_id": game_id}).sort("timestamp"))

    def find_by_game_id_since(self, game_id, since):
        return list(
            self.collection
            .find(
                {
                    "game_id": game_id,
                    "timestamp": {"$gte": since}
                }
            )
            .sort("timestamp")
        )

    def find_latest_record_by_game_id(self, game_id, sort_by, direction=-1):
        results = list(
            self.collection
            .find({"game_id": game_id})
            .sort(sort_by, direction)
            .limit(1)
        )

        if not len(results):
            return None

        return results[0]

    def delete_by_game_id(self, game_id):
        self.collection.delete_many({"game_id": game_id})

    def save(self, models):

        if not len(models):
            return

        start = time.perf_counter()

        def update_action(model):
            return UpdateOne({"id": model["id"]}, {"$set": model}, True)

        self.collection.bulk_write(
            list(map(lambda model: update_action(model), models))
        )

        logging.info(
            f"⏱  [PriceRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s"
        )
