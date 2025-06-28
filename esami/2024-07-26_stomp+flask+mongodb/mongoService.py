from pymongo import MongoClient
from pymongo.database import Database


class MongoService:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        self.client: MongoClient = None
        self.db: Database = None

    def getDatabase(self, dbName: str) -> Database:
        self.client = MongoClient(f"mongodb://{self.address}:{self.port}")
        if self.client == None:
            return None

        self.db = self.client[dbName]
        return self.db

    def closeConnection(self):
        if self.client == None:
            return

        self.db = None
        self.client.close()
