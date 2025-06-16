from flask import Flask, request
from database.mongoService import MongoService
from pymongo.errors import DuplicateKeyError, PyMongoError

from dataType.dataType import DataType

HOST_MONGO = "127.0.0.1"
PORT_MONGO = 27017

DB_NAME = "SensorDataDB"

SENSORS_COLLETION = "sensors"
TEMP_DATA_COLLECTION = "temp_data"
PRESS_DATA_COLLECTION = "press_data"

app = Flask(__name__)


@app.post("/sensor")
def createSensor():
    sensor = request.json
    print(
        f"[CONTROLLER] Ho ricevuto una richiesta POST su /sensor con body json: {sensor}"
    )

    sensorCollection = db[SENSORS_COLLETION]

    try:

        print(f"[CONTROLLER] Inserisco nel database il sensore {sensor}")
        sensorCollection.insert_one(sensor)
        print(f"[CONTROLLER] Inserito correttamente!")

    except DuplicateKeyError as e:
        print("[CONTROLLER] Il sensore è già registrato nel database!")
        return {"result": "duplicate sensor"}, 400
    except PyMongoError as e:
        print(f"[CONTROLLER] Errore di pymongo: {e}")
        return {"result": "database error"}, 500

    return {"result": "success"}, 200


@app.post("/data/<data_type>")
def createSensorData(data_type):
    sensor_data = request.json
    print(
        f"[CONTROLLER] Ho ricevuto una richiesta POST su /data/{data_type} con body json: {sensor_data}"
    )

    try:
        dataType = DataType(data_type)
    except ValueError as e:
        print(f"[CONTROLLER] Tipo di dato non riconosciuto")
        return {"result": "invalid data_type"}, 400

    match (dataType):
        case DataType.TEMPERATURE:
            collectionName = TEMP_DATA_COLLECTION
        case DataType.PRESSURE:
            collectionName = PRESS_DATA_COLLECTION

    collection = db[collectionName]

    try:

        print(f"[CONTROLLER] Inserisco nel database i dato del sensore {sensor_data}")
        collection.insert_one(sensor_data)

    except PyMongoError as e:
        print(f"[CONTROLLER] Errore di pymongo: {e}")
        return {"result": "database error"}, 500

    return {"result": "success"}, 200


if __name__ == "__main__":
    mongoService = MongoService(HOST_MONGO, PORT_MONGO)
    db = mongoService.getDatabase(DB_NAME)

    app.run(debug=True)
