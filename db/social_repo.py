import logging
from ekp_sdk.db import MgClient
from pymongo import UpdateOne
import time


class SocialRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['socials']
        self.collection.create_index("id", unique=True)
        self.collection.create_index("timestamp")
        self.collection.create_index("game_id")
        self.collection.create_index("platform")

    def find_latest_by_game_id(self, platform):
        start = time.perf_counter()

        results = list(
            self.collection
            .aggregate([
                {"$sort": {"timestamp": 1}},
                {
                    "$group":
                    {
                        "_id": "$game_id",
                        "members": {"$last": "$members"}
                    }
                }
            ])
        )

        logging.info(
            f"⏱  [SocialRepo.find_latest_by_game_id({platform})] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return None

        return results

    def find_latest(self, game_id, platform):
        start = time.perf_counter()

        results = list(
            self.collection
            .find({
                "game_id": game_id,
                "platform": platform
            })
            .sort('timestamp', -1)
            .limit(1)
        )

        logging.info(
            f"⏱  [SocialRepo.find_latest({game_id}, {platform})] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return None
        
        return results[0]
    
    def save(self, models):
        start = time.perf_counter()

        def update_action(model):
            return UpdateOne({"id": model["id"]}, {"$set": model}, True)

        self.collection.bulk_write(
            list(map(lambda model: update_action(model), models))
        )

        logging.info(
            f"⏱  [SocialRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s")
