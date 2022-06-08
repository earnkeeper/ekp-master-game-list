import logging
from ekp_sdk.db import MgClient
import time

class RoadmapEventRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['roadmap_events']
        self.collection.create_index("timestamp")
        self.collection.create_index("game_id")

    def find_all(self):
        return list(
            self.collection.find().sort("timestamp")
        )
    
    def find_by_game_id(self, game_id):
        return list(self.collection.find({ "game_id": game_id }).sort("timestamp"))
        
    def delete_by_game_id(self, game_id):
        self.collection.delete_many({ "game_id": game_id })
        
    def save(self, models):
        if not len(models):
            logging.warn("⚠️ [RoadmapEventRepo.save()] skipping save due to empty records passed to method")
            return
        
        start = time.perf_counter()

        with self.mg_client.client.start_session() as session:
            with session.start_transaction():
                self.collection.drop()
                self.collection.insert_many(models)
                
        print(
            f"⏱  [RoadmapEventRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s"
        )


