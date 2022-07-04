import logging
import time
from pymongo import UpdateOne

from db.mg_client_eth import MgClientEth


class GameRepoEth:
    def __init__(
            self,
            mg_client: MgClientEth,
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

    def save(self, models):
        
        if not len(models):
            return
        
        start = time.perf_counter()

        def update_action(model):
            new_model = model
            del new_model["_id"]
            return UpdateOne({ "id": model["id"]}, {"$set": model}, True)

        self.collection.bulk_write(
            list(map(lambda model: update_action(model), models))
        )

        logging.info(f"⏱  [GameRepoEth.save({len(models)})] {time.perf_counter() - start:0.3f}s")