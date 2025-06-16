import grpc

from concurrent import futures
from typing import Iterator

import gRPC.statistics_pb2 as statistics
import gRPC.statistics_pb2_grpc as statistics_grpc

from pymongo.database import Database
from database.mongoService import MongoService

from dataType.dataType import DataType

HOST_MONGO = "127.0.0.1"
PORT_MONGO = 27017

DB_NAME = "SensorDataDB"

PORT_GRPC = 0

SENSORS_COLLETION = "sensors"
TEMP_DATA_COLLECTION = "temp_data"
PRESS_DATA_COLLECTION = "press_data"


class StatisticsServicerImpl(statistics_grpc.StatisticsServiceServicer):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db

    def getSensors(
        self, request: statistics.Empty, context: grpc.ServicerContext
    ) -> Iterator[statistics.Sensor]:

        print(f"[STATISTICS] Ricevuta richiesta getSensors")

        sensorCollection = self.db[SENSORS_COLLETION]

        try:

            print(f"[STATISTICS] Cerco tutti i sensori")
            sensors = sensorCollection.find()
            count = 0

            for sensorDocument in sensors:
                count += 1
                print(f"[STATISTICS] Invio il sensore {sensorDocument}")
                sensor = statistics.Sensor(
                    _id=sensorDocument["_id"], data_type=sensorDocument["data_type"]
                )
                yield sensor

            if count == 0:
                print(f"[STATISTICS] Non ci sono sensori")
                yield statistics.Sensor(_id=-1, data_type="NO_SENSORS")

        except PyMongoError as e:
            print(f"[STATISTICS] Errore di pymongo: {e}")
            return [statistics.Sensor(_id=-1)]

    def getMean(
        self, request: statistics.MeanRequest, context: grpc.ServicerContext
    ) -> statistics.StringMessage:

        print(
            f"[STATISTICS] Ricevuta richiesta getMean con sensor_id = {request.sensor_id} e data_type = {request.data_type}"
        )

        sensor_id = request.sensor_id

        try:
            dataType = DataType(request.data_type)
        except ValueError:
            print(f"[STATISTICS] data_type del sensore non riconosciuto")
            return statistics.StringMessage(value="Tipo non riconosciuto")

        match dataType:
            case DataType.TEMPERATURE:
                collectionName = TEMP_DATA_COLLECTION
            case DataType.PRESSURE:
                collectionName = PRESS_DATA_COLLECTION

        dataCollection = self.db[collectionName]

        try:
            print(
                f"[STATISTICS] Cerco tutte le misurazioni del sensore {sensor_id} con data_type {str(dataType)}"
            )
            datas = dataCollection.find()

            data_mean = 0
            data_count = 0
            for dataDocument in datas:
                print(f"[STATISTICS] Data {dataDocument}")
                data_mean += int(dataDocument["data"])
                data_count += 1

            data_mean /= data_count

            print(f"[STATISTICS] Invio la media delle misurazioni: {data_mean}")
            return statistics.StringMessage(value=str(data_mean))

        except PyMongoError as e:
            print(f"[STATISTICS] Errore di pymongo: {e}")
            return statistics.StringMessage(value="Errore di database")


if __name__ == "__main__":
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))

    mongoService = MongoService(HOST_MONGO, PORT_MONGO)
    db = mongoService.getDatabase(DB_NAME)
    servicer = StatisticsServicerImpl(db)

    statistics_grpc.add_StatisticsServiceServicer_to_server(servicer, server)

    PORT_GRPC = server.add_insecure_port(f"[::]:{PORT_GRPC}")

    server.start()

    print(f"[STATISTICS] In ascolto sulla porta {PORT_GRPC}...")

    server.wait_for_termination()

    print(f"[STATISTICS] Non più in ascolto...")

    server.stop()

    mongoService.closeConnection()
