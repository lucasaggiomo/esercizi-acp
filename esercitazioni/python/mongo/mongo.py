from pymongo import MongoClient
from typing import Optional


# classe per incapsulare l'ottenimento del database mongodb
class MongoService:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client: Optional[MongoClient] = None
        self._connect()

    def _connect(self):
        if not self.client:
            self.client = MongoClient(self.host, self.port)

    def getDatabase(self, dbName: str):
        if not self.client:
            self._connect()

        return self.client[dbName]

    def closeConnection(self):
        if self.client:
            self.client.close()
            self.client = None


if __name__ == "__main__":
    mongoService = MongoService("localhost", 27017)
    db = mongoService.getDatabase("HistoryDB")

    laptopCollection = db["laptopHistory"]
    result = laptopCollection.find({"serial_number": 10})

    print(type(result))

    print(len(result))

    mongoService.closeConnection()
