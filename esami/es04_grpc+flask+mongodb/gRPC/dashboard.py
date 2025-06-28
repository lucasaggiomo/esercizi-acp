import grpc
import sys

from typing import Iterator

import gRPC.statistics_pb2 as statistics
import gRPC.statistics_pb2_grpc as statistics_grpc

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            HOST = "localhost"
            PORT = int(sys.argv[1])
        elif len(sys.argv) >= 3:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
    except:
        print(
            "Inserisci il numero di porta come primo argomento (default grpc) oppure l'host seguito dal numero di porta"
        )
        sys.exit(1)

    with grpc.insecure_channel(target=f"{HOST}:{PORT}") as channel:
        stub = statistics_grpc.StatisticsServiceStub(channel)

        empty = statistics.Empty()
        sensors: Iterator[statistics.Sensor] = stub.getSensors(empty)

        print(f"Questi sono i sensori registrati:")
        for sensor in sensors:
            if sensor._id == -1:
                break

            print(f"_id: {sensor._id}, data_type: {sensor.data_type}")

            meanRequest = statistics.MeanRequest(
                sensor_id=sensor._id, data_type=sensor.data_type
            )
            meanMessage: statistics.StringMessage = stub.getMean(meanRequest)
            mean = float(meanMessage.value)

            print(f"\tMedia misurazioni: {mean}")

        print("Fine")
