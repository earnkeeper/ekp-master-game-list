import logging
import time
from ekp_sdk.db import MgClient
from pymongo import UpdateOne


class YoutubeRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.collection = self.mg_client.db['youtube_game_list']
        self.collection.create_index("id", unique=True)
        self.collection.create_index("game_name")
        self.collection.create_index("view_count")
        self.collection.create_index("publish_time")


    def find_all(self):
        return list(self.collection.find())

    def find_one_by_id(self, id):
        return self.collection.find_one({"id": id})

    def delete_records(self):
        self.collection.delete_many({})

    def save(self, videos):
        start = time.perf_counter()

        self.collection.bulk_write(
            list(map(lambda video: UpdateOne({"id": video["id"]}, {"$set": video}, True), videos))
        )

        print(f"⏱  [YoutubeRepo.save({len(videos)})] {time.perf_counter() - start:0.3f}s")