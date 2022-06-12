import logging
import time
from ekp_sdk.db import MgClient
from pymongo import UpdateOne

class GameRepo:
    def __init__(
        self,
        mg_client: MgClient
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
        return self.collection.find_one({ "id": id })
    
    def upsert(self, game):
        start = time.perf_counter()
        
        self.collection.update_one({ "id": game["id"]}, {"$set": game}, True)

        logging.info(f"⏱  [GameRepo.upsert({game['id']})] {time.perf_counter() - start:0.3f}s")