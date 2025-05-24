from flask_mongo_grpc.database.IdbManager import IDBManager
from flask_mongo_grpc.utils.dataTypes import DataType
from pymongo import MongoClient

ADDRESS = "192.168.43.129"
PORT = "27017"


class MongoDBManager(IDBManager):
    SENSORS_COLLECTION_NAME = "sensors"

    def __init__(self, dbName):
        self.dbName = dbName
        self.client = MongoClient(f"mongodb://{ADDRESS}:{PORT}")
        self.db = self.client[dbName]

    @staticmethod
    def getCollectionNameFromDataType(dataType: DataType):
        return f"{str(dataType)}_data"

    def closeConnection(self):
        self.client.close()

    def addSensor(self, sensor):
        self.db[MongoDBManager.SENSORS_COLLECTION_NAME].insert_one(sensor)

    def addMeasurement(self, measure, dataType: DataType):
        collectionName = MongoDBManager.getCollectionNameFromDataType(dataType)
        self.db[collectionName].insert_one(measure)

    def getAllSensors(self):
        return self.db[MongoDBManager.SENSORS_COLLECTION_NAME].find()

    def getAllMeasurements(self, sensorId: int, dataType: DataType):
        collectionName = MongoDBManager.getCollectionNameFromDataType(dataType)
        return self.db[collectionName].find()

    def doQuery(self, collection_name, **kwargs):
        collection = self.db[collection_name]
        return collection.find(kwargs)
