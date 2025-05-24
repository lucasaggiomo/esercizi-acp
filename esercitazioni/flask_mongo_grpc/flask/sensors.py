import random
import threading as th

import requests
from flask_mongo_grpc.utils.dataTypes import DataType

NUM_THREADS = 5
NUM_MEASUREMENTS = 5
SERVER_ADDRESS = "http://127.0.0.1:5000"


def addSensor(sensor_id: int, data_type: DataType):
    request = {"_id": sensor_id, "data_type": str(data_type)}
    response = requests.post(f"{SERVER_ADDRESS}/sensor", json=request)

    try:
        response.raise_for_status()
        print(
            f"[ADD_SENSOR] Ricevuta la risposta: {response.text}, status code: {response.status_code}"
        )
    except requests.exceptions.HTTPError:
        print(
            f"[ADD_SENSOR] Errore nella risposta: {response.text}, status_code: {response.status_code}"
        )
    except Exception as e:
        print(f"[ADD_SENSOR] Errore generico: {e}")


def addMeasurement(sensor_id: int, data: int, data_type: DataType):
    request = {"sensor_id": sensor_id, "data": data}
    response = requests.post(f"{SERVER_ADDRESS}/data/{str(data_type)}", json=request)

    try:
        response.raise_for_status()
        print(
            f"[ADD_MEASUREMENT] Ricevuta la risposta: {response.text}, status code: {response.status_code}"
        )
    except requests.exceptions.HTTPError:
        print(
            f"[ADD_MEASUREMENT] Errore nella risposta: {response.text}, status_code: {response.status_code}"
        )
    except Exception as e:
        print(f"[ADD_MEASUREMENT] Errore generico: {e}")


def threadFunction(sensor_id: int, data_type: DataType, num_measurements: int):
    addSensor(sensor_id, data_type)

    for _ in range(num_measurements):
        data = random.randint(1, 50)
        addMeasurement(sensor_id, data, data_type)


if __name__ == "__main__":
    threadList: list[th.Thread] = []
    for id in range(NUM_THREADS):
        data_type = random.choice(list(DataType))
        t = th.Thread(target=threadFunction, args=(id, data_type, NUM_MEASUREMENTS))
        threadList.append(t)
        t.start()

    for t in threadList:
        t.join()
    for t in threadList:
        t.join()
