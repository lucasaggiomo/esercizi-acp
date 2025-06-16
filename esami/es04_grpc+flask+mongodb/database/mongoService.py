from pymongo import MongoClient
from pymongo.database import Database

# classe per incapsulare la connessione al database mongodb
class MongoService:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.client = MongoClient(f"mongodb://{host}:{port}")
        self.db: Database = None

    def getDatabase(self, dbName: str) -> Database:
        self.db = self.client[dbName]
        return self.db

    def closeConnection(self):
        if self.client != None:
            self.db = None
            self.client.close()
