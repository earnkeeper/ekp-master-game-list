from pymongo import MongoClient


class ServerMgClient:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        print("👍 Connected to Server MongoDb")