import abc
from typing import Any

from flask_mongo_grpc.utils.dataTypes import DataType


class IDBManager(abc.ABC):
    @abc.abstractmethod
    def closeConnection(self):
        pass

    @abc.abstractmethod
    def addSensor(self, sensor):
        pass

    @abc.abstractmethod
    def addMeasurement(self, measure, dataType: DataType):
        pass

    @abc.abstractmethod
    def getAllSensors(self) -> Any:
        pass

    @abc.abstractmethod
    def getAllMeasurements(self, sensorId: int, dataType: DataType) -> Any:
        pass

    # funzione per fare query generiche
    @abc.abstractmethod
    def doQuery(self, collection_name, **kwargs) -> Any:
        pass
