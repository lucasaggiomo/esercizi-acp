from pymongo import MongoClient
from pymongo.database import Database


class MongoService:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = None

    def getDatabase(self, dbName: str) -> Database:
        self.client = MongoClient(f"mongodb://{self.host}:{self.port}")
        self.db = self.client[dbName]
        return self.db

    def closeConnection(self):
        self.client.close()
