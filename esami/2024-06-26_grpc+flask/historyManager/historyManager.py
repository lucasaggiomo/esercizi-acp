from flask import Flask, request
from operation import Operation

app = Flask(__name__)

HISTORY_FILE_PATH = "history.txt"


def logHistory(operation: Operation, serial_number: int):
    message = f"{str(operation)}-{serial_number}"

    with open(HISTORY_FILE_PATH, mode="a") as historyFile:
        historyFile.write(message + "\n")


@app.post("/")
def handlePostRequest():
    # riconosce l'operazione effettuata
    body = request.get_json()
    print("[HISTORY_MANAGER] Ho ricevuto una richiesta POST con body: ", body)

    try:
        try:
            operation = Operation(body["operation"])
        except ValueError:
            print("[HISTORY_MANAGER] Operazione non riconosciuta")
            return {"result": "Operazione non riconsociuta"}, 400

        serial_number = body["serial_number"]

        # inserisce nella history
        logHistory(operation, serial_number)

        return {"result": "Successful"}, 200

    except KeyError as e:
        print(
            f"[HISTORY_MANAGER] Il json è diverso da come mi aspettavo (dovrebbe esserci 'operation' (str) e 'serial_number' (int)) [errore interno: {e}]"
        )
        return {"result": "Body errato"}, 400


if __name__ == "__main__":
    app.run(debug=True)
