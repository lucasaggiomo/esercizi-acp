import requests
import threading as th
import random

from dataType.dataType import DataType

NUM_SENSORI = 5
NUM_MISURAZIONI = 5

HOST_CONTROLLER = "127.0.0.1"
PORT_CONTROLLER = 5000


class SensorThread(th.Thread):
    def __init__(
        self, id: int, dataType: DataType, host: str, port: int, numMisurazioni: int
    ):
        super().__init__()
        self.id = id
        self.dataType = dataType
        self.host = host
        self.port = port
        self.numMisurazioni = numMisurazioni

    # stub per ottenere la misurazione
    def getData(self):
        return random.randint(1, 50)

    def run(self):
        # effettua la registrazione presso /sensor
        sensorJson = {"_id": self.id, "data_type": str(self.dataType)}

        try:
            print(f"[SENSOR - {self.id}] Mi registro come sensore: {sensorJson}")
            response = requests.post(
                f"http://{self.host}:{self.port}/sensor", json=sensorJson
            )
            response.raise_for_status()
            print(
                f"[SENSOR - {self.id}] Ho ricevuto: {response.json()}, status_code = {response.status_code}"
            )
        except requests.HTTPError as e:
            print(
                f"[SENSOR - {self.id}] Errore nella registrazione del sensore: {response.json()}, status_code = {response.status_code}"
            )

            if response.json()["result"] != "duplicate sensor":
                return

        # effettua cinque misurazioni presso /data/<data_type>
        for _ in range(self.numMisurazioni):
            data = self.getData()
            dataJson = {"sensor_id": self.id, "data": data}
            try:
                print(f"[SENSOR - {self.id}] Invio la misurazione: {dataJson}")
                response = requests.post(
                    f"http://{self.host}:{self.port}/data/{str(self.dataType)}",
                    json=dataJson,
                )
                response.raise_for_status()
            except requests.HTTPError as e:
                print(
                    f"[SENSOR - {self.id}] Errore nella registrazione della misurazione: {response.json()}, status_code = {response.status_code}"
                )
                return


if __name__ == "__main__":

    threads: list[th.Thread] = []

    print("[SENSORS] Inizio l'esecuzione")

    for i in range(NUM_SENSORI):
        sensor_id = i
        sensor_data_type = random.choice(list(DataType))

        sensorThread = SensorThread(
            id=sensor_id,
            dataType=sensor_data_type,
            host=HOST_CONTROLLER,
            port=PORT_CONTROLLER,
            numMisurazioni=NUM_MISURAZIONI,
        )
        sensorThread.start()
        threads.append(sensorThread)

    for t in threads:
        t.join()

    print("[SENSORS] Termino l'esecuzione")
