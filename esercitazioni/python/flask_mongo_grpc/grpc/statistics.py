import sys
import time
from concurrent import futures
from typing import Iterator

import flask_mongo_grpc.grpc.service_pb2 as service_pb2
import flask_mongo_grpc.grpc.service_pb2_grpc as service_pb2_grpc
import grpc
from flask_mongo_grpc.database.mongodbManager import MongoDBManager
from flask_mongo_grpc.utils.dataTypes import DataType


class ServiceStats(service_pb2_grpc.SensorServiceServicer):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def getSensors(self, request: service_pb2.Empty, context) -> Iterator[service_pb2.Sensor]:
        print("[STATS] Received request of all sensors")

        # legge tutti i sensori presenti in getSensors e yielda messaggi Sensor
        sensors = db.getAllSensors()
        for sensor in sensors:
            print(f"\t[STATS] Sensor {sensor["_id"]}, {sensor["data_type"]}")
            sensorResponse = service_pb2.Sensor(_id=sensor["_id"], dataType=sensor["data_type"])
            yield sensorResponse

    def getMean(self, request: service_pb2.MeanRequest, context) -> service_pb2.StringMessage:
        sensor_id = request.sensor_id
        data_type = DataType(request.dataType)

        print(f"[STATS] Received request of mean of sensor {sensor_id}, data_type = {data_type}")

        # calcola la media delle misure effettuate dal sensore con id sensor_id
        measures = db.getAllMeasurements(sensor_id, data_type)
        mean = 0
        counter = 0
        for measure in measures:
            print(f"\t[STATS] Measure {measure["data"]}")
            mean += measure["data"]
            counter += 1
        mean /= counter

        return service_pb2.StringMessage(value=str(mean))


if __name__ == "__main__":
    PORT = 0

    try:
        DB_NAME = sys.argv[1]
    except IndexError:
        print("Inserisci il nome del database")
        sys.exit(1)

    db = MongoDBManager(DB_NAME)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = ServiceStats(db)
    PORT = server.add_insecure_port(f"[::]:{PORT}")

    service_pb2_grpc.add_SensorServiceServicer_to_server(servicer, server)

    print("[STATS] Running on port " + str(PORT))

    server.start()

    server.wait_for_termination()
