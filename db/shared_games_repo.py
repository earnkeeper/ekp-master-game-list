import logging
import time
from ekp_sdk.db import MgClient
from pymongo import UpdateOne


class SharedGamesRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['shared_games']
        self.collection.create_index("game_id")
        self.collection.create_index("date_timestamp")
        # self.collection.create_index("source")

    def find_all(self):
        return list(self.collection.find({
            "disable": False
        }))


    def find_game_ids_with_shared_games_today(self, midnight):
        results = list(
            self.collection
            .aggregate([
                {
                    "$match": {
                        "date_timestamp": midnight,
                    }
                },
                {
                    "$group":
                    {
                        "_id": "$game_id",
                    }
                }
            ])
        )

        if not len(results):
            return []

        return list(
            map(
                lambda x: x["_id"],
                results
            )
        )

    def delete_where_timestamp_before(self, midnight):
        self.collection.delete_many(
            {
                "date_timestamp": {
                    "$lt": midnight
                }
            }
        )

    def upsert(self, game):
        start = time.perf_counter()

        self.collection.update_one({"id": game["id"]}, {"$set": game}, True)

        logging.info(f"⏱  [GameRepo.upsert({game['id']})] {time.perf_counter() - start:0.3f}s")

    def save(self, models):

        start = time.perf_counter()

        if not len(models):
            return

        self.collection.insert_many(models)

        logging.info(f"⏱  [SharedGamesRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s")
