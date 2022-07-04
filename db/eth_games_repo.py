import logging
import time
from ekp_sdk.db import MgClient
from pymongo import UpdateOne

from db.server_mg_client import ServerMgClient


class EthGamesRepo:
    def __init__(
            self,
            mg_client: ServerMgClient,
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['master_game_list']
        self.collection.create_index("id", unique=True)
        self.collection.create_index("source")

    def find_all(self):
        return list(self.collection.find({
            "disable": False
        }))

    def find_one_by_id(self, id):
        return self.collection.find_one({"id": id})

    def save(self, games):
        start = time.perf_counter()

        self.collection.insert_many(games)

        logging.info(f"⏱  [EthGamesRepo.upsert({len(games)})] {time.perf_counter() - start:0.3f}s")