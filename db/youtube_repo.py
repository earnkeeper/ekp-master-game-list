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
    
    def find_game_ids_with_videos_today(self, midnight):
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


        # [{"_id": "metabomb"}, {"_id": "mines-of-dalarnia"}]
        # ["metabomb", "mines-of-dalarnia"]
        
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

    def find_videos_by_game_name(self, game_name):
        results = list(
            self.collection
                .find({"game_name": game_name},
                      {"_id": False})
                .limit(10)
        )

        if not len(results):
            return []

        return results

    def delete_records(self):
        self.collection.delete_many({})

    def save(self, videos):
        start = time.perf_counter()

        self.collection.bulk_write(
            list(map(lambda video: UpdateOne({"id": video["id"]}, {"$set": video}, True), videos))
        )

        print(f"⏱  [YoutubeRepo.save({len(videos)})] {time.perf_counter() - start:0.3f}s")
