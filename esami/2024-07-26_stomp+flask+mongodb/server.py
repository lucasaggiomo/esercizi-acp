from flask import Flask, request
from mongoService import MongoService
import time

app = Flask(__name__)

ADDRESS_MONGO = "127.0.0.1"
PORT_MONGO = 27017
DB_NAME = "PrenotazioniDB"


@app.post("/")
def createPrenotazione():
    print("[SERVER] Ho riceuvo una POST con json: " + str(request.json))
    prenotazione = request.json

    database = mongoService.getDatabase(DB_NAME)

    # crea una nuova prenotazione
    try:
        result = database["Prenotazioni"].insert_one(prenotazione)
        return {"result": "Creata prenotazione con id " + str(result.inserted_id)}, 200

    except Exception as e:
        print("[SERVER] Errore nella create: " + str(e))

        # errore di Server
        return {"result": "Database error"}, 500


@app.put("/")
def updatePrenotazione():
    print("[SERVER] Ho riceuvo una PUT con json: " + str(request.json))
    query = request.json

    database = mongoService.getDatabase(DB_NAME)

    # applica lo sconto a tutte le prenotazioni create dall’operatore specificato nel body
    # richiesta e che abbiano almeno un numero di notti maggiore o uguale al valore specificato nel
    # body della richiesta. Per tutte le prenotazioni trovate, il costo della prenotazione viene aggiornato
    # sottraendo al costo attuale il discount ricevuto nel body della richiesta (impostando a zero il
    # costo, se la sottrazione porta ad un risultato negativo).
    try:
        operator = query["operator"]
        minNights = query["nights"]
        discount = query["discount"]
    except KeyError as e:
        print("[SERVER] Errore di chiave: " + str(e))

        # errore di BadRequest
        return {"result": "KeyError"}, 400

    try:
        result = database["Prenotazioni"].find(
            {"operator": operator, "nights": {"$gte": minNights}}
        )

        count = 0

        for document in result:
            count += 1
            newCost = document.get("cost") - discount
            if newCost < 0:
                newCost = 0
            database["Prenotazioni"].update_one(document, {"$set": {"cost": newCost}})

        return {
            "result": f"Applicato lo sconto di {discount} a {count} prenotazioni"
        }, 200

    except Exception as e:
        print("[SERVER] Errore nella update: " + str(e))

        # errore di Server
        return {"result": "Database error"}, 500


if __name__ == "__main__":
    mongoService = MongoService(ADDRESS_MONGO, PORT_MONGO)

    app.run(debug=True)

    while True:
        time.sleep(60)

    mongoService.closeConnection()
