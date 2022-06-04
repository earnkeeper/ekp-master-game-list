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

    def find_by_source(self, source):
        return list(self.collection.find({ source: "source" }))
    
    def delete_by_id(self, id):
        self.collection.delete_many({ "id": id })
        
    def save(self, models):
    
        def update_action(model):
            return UpdateOne({ "id": model["id"]}, {"$set": model}, True)

        self.collection.bulk_write(
            list(map(lambda model: update_action(model), models))
        )
