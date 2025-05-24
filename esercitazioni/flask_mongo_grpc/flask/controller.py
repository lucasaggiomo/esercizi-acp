import sys
from typing import Any

from flask import Flask, request
from flask_mongo_grpc.database.mongodbManager import MongoDBManager
from flask_mongo_grpc.utils.dataTypes import DataType

app = Flask(__name__)


@app.post("/sensor")
def addSensor() -> Any:
    global db
    try:
        sensor = request.get_json()
    except Exception as e:
        print(f"Errore nella json: {e}")
        return {"result": f"failed = {e}"}, 400

    try:
        sensor_id = sensor["_id"]
        data_type = DataType(sensor["data_type"])
        print(f"[ADD SENSOR] Ho ottenuto un sensore {sensor}")
    except KeyError:
        print(f"[ADD SENSOR] Bad request, sensor was {sensor}")
        return {"result": "failed"}, 400
    except Exception as e:
        print(f"Errore generico: {e}")
        return {"result": f"failed = {e}"}, 400

    try:
        db.addSensor(sensor)

        return "{'result': 'success'}", 201
    except Exception as e:
        print("[ADD SENSOR] Problem with addSensor")
        return {"result": f"failed = {e}"}, 500


@app.post("/data/<data_type>")
def addMeasurement(data_type: str):
    global db
    dataType = DataType(data_type)
    try:
        measure = request.get_json()
    except Exception as e:
        print(f"Errore nella json: {e}")
        return {"result": f"failed = {e}"}, 400

    try:
        sensor_id = measure["sensor_id"]
        data = measure["data"]
        print(f"[ADD SENSOR] Ho ottenuto la misurazione {measure}")
    except KeyError:
        print(f"[ADD SENSOR] Bad request, measure was {measure}")
        return {"result": "failed"}, 400
    except Exception as e:
        print(f"Errore generico: {e}")
        return {"result": f"failed = {e}"}, 400

    try:
        db.addMeasurement(measure, dataType)

        return "{'result': 'success'}", 201
    except Exception as e:
        print("[ADD MEASUREMENT] Problem with addMeasurement")
        return {"result": f"failed = {e}"}, 500


if __name__ == "__main__":
    try:
        DB_NAME = sys.argv[1]
    except IndexError:
        print("Inserisci il nome del database")
        sys.exit(1)

    db = MongoDBManager(DB_NAME)

    app.run(debug=True)

    db.closeConnection()
