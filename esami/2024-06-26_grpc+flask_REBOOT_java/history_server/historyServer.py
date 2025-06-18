from flask import Flask, request

app = Flask(__name__)


@app.post("/update_history")
def update_history():
    json = request.get_json(silent=True)
    if json == None:
        return {"result", "Invalid or missing JSON"}, 400
    print(f"[HISTORY-MANAGER] Ho ricevuto il messaggio {json}")

    tipo = json["operation"]
    serialNumber = json["serial_number"]

    with open("history.txt", "a") as file:
        file.write(f"{tipo}-{serialNumber}\n")

    return {"result": "success"}, 200


if __name__ == "__main__":
    app.run(debug=True)
