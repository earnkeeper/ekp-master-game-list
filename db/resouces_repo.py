import logging
import time
from ekp_sdk.db import MgClient
from pymongo import UpdateOne


class ResourcesRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['game_resources']
        self.collection.create_index("game_id")


    def find_resources_by_game_id(self, game_id):

        return list(self.collection.find({"game_id": game_id},
                                    {"_id": False}))

    def save(self, resources):
        start = time.perf_counter()

        self.collection.bulk_write(
            list(map(lambda resource: UpdateOne(
                {"game_id": resource["game_id"],
                 "rank": resource["rank"]
                 }, {"$set": resource}, True), resources))
        )

        logging.info(f"⏱  [ResourcesRepo.update({len(resources)})] {time.perf_counter() - start:0.3f}s")
