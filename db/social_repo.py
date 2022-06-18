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

    def find_by_game_id(self, game_id):
        return list(self.collection.find({"game_id": game_id}))

    def find_latest_for_game_id(self, game_id):
        start = time.perf_counter()

        results = list(
            self.collection
            .find({"game_id": game_id, "twitter_followers": {"$exists": True}})
            .sort("timestamp",-1)
            .limit(1)
        )

        logging.info(
            f"⏱  [SocialRepo.find_latest_by_game_id()] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return None

        return results[0]

    def find_latest_group_by_game_id(self):
        start = time.perf_counter()

        results = list(
            self.collection
            .aggregate([
                {"$sort": {"timestamp": 1}},
                {
                    "$group":
                    {
                        "_id": "$game_id",
                        "twitter_followers": {"$last": "$twitter_followers"},
                        "telegram_members": {"$last": "$telegram_members"},
                    }
                }
            ])
        )

        logging.info(
            f"⏱  [SocialRepo.find_latest_by_game_id()] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return []

        return results

    def find_chart_for_game_id(self, game_id):
        start = time.perf_counter()

        results = list(
            self.collection
            .aggregate([
                {
                    "$match": {"game_id": game_id}
                },
                {
                    "$sort": {"timestamp": 1}
                },
                {
                    "$group":
                    {
                        "_id": "$date_timestamp",
                        "value": {"$last": "$twitter_followers"}
                    }
                }
            ])
        )

        logging.info(
            f"⏱  [SocialRepo.find_chart_by_game_id()] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return []

        return results

    def group_by_date(self, game_id):
        start = time.perf_counter()

        results = list(
            self.collection
            .aggregate([
                {
                    "$match": {
                        "date_timestamp": {"$exists": True},
                        "twitter_followers": {
                            "$exists": True,
                            "$ne": None
                        },
                        "game_id": game_id,
                    }
                },
                {"$sort": {"date_timestamp": 1}},
                {
                    "$group":
                    {
                        "_id": "$date_timestamp",
                        "value": {"$avg": "$twitter_followers"}
                    }
                }
            ])
        )

        logging.info(
            f"⏱  [SocialRepo.group_by_game_id_and_date()] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return []

        return results
    
    def group_by_game_id_and_date(self):
        start = time.perf_counter()

        results = list(
            self.collection
            .aggregate([
                {
                    "$match": {"date_timestamp": {"$exists": True}}
                },
                {"$sort": {"date_timestamp": 1}},
                {
                    "$group":
                    {
                        "_id": {"game_id": "$game_id", "date_timestamp": "$date_timestamp"},
                        "value": {"$avg": "$twitter_followers"}
                    }
                }
            ])
        )

        logging.info(
            f"⏱  [SocialRepo.group_by_game_id_and_date()] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return []

        return results

    def find_all_since(self, timestamp):
        start = time.perf_counter()

        results = list(
            self.collection
            .find({
                "timestamp": {
                    "$gte": timestamp
                }
            })
            .sort('timestamp')
        )

        logging.info(
            f"⏱  [SocialRepo.find_all_by_game_id({timestamp})] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return []

        return results
    
    def find_all_since_for_game_id(self, timestamp, game_id):
        start = time.perf_counter()

        results = list(
            self.collection
            .find({
                "timestamp": {
                    "$gte": timestamp
                },
                "game_id": game_id
            })
            .sort('timestamp')
        )

        logging.info(
            f"⏱  [SocialRepo.find_all_by_game_id({timestamp})] {time.perf_counter() - start:0.3f}s"
        )

        if not results or not len(results):
            return []

        return results

    def find_latest(self, game_id):
        start = time.perf_counter()

        results = list(
            self.collection
            .find({
                "game_id": game_id,
            })
            .sort('timestamp', -1)
            .limit(1)
        )

        logging.info(
            f"⏱  [SocialRepo.find_latest({game_id})] {time.perf_counter() - start:0.3f}s"
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
