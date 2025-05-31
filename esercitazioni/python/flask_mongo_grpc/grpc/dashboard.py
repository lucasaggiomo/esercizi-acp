import sys

import flask_mongo_grpc.grpc.service_pb2 as service_pb2
import flask_mongo_grpc.grpc.service_pb2_grpc as service_pb2_grpc
import grpc


def run(port: int):
    with grpc.insecure_channel(f"localhost:{port}") as channel:

        stub = service_pb2_grpc.SensorServiceStub(channel)

        print("[DASHBOARD] Sending request for available sensors")
        sensors_response = stub.getSensors(service_pb2.Empty())

        sensors: list[service_pb2.Sensor] = []
        for sensor in sensors_response:
            print(f"[DASHBOARD] Sensor: {sensor._id}, {sensor.dataType}")
            sensors.append(sensor)

        for sensor in sensors:
            response: service_pb2.StringMessage = stub.getMean(
                service_pb2.MeanRequest(sensor_id=sensor._id, dataType=sensor.dataType)
            )
            print(f"[DASHBOARD] Sensor: {sensor._id}, {sensor.dataType}, mean = {response.value}")


if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except:
        print("Insert port as first argument")
        sys.exit(1)

    run(PORT)
