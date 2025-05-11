import random
import uuid

import stomp
from products import ProductType

MAX_VALUE = 1 << 63

class ResponseListener(stomp.ConnectionListener):
    def __init__(self):
        pass

    def on_message(self, frame):
        msg = frame.body

        print(f"[CLIENT] Ho ricevuto {msg}")


if __name__ == "__main__":
    conn = stomp.Connection([("127.0.0.1", 61613)])
    conn.connect(wait=True)

    conn.subscribe(destination="/queue/responses", id=1, ack="auto")
    conn.set_listener("listener", ResponseListener())

    for _ in range(10):
        idItem = int(uuid.uuid1()) % MAX_VALUE
        articolo = random.choice(list(ProductType))
        msg = f"Deposita-{idItem}-{articolo}"
        conn.send(destination="/queue/requests", body=msg)
        print(f"[CLIENT] Ho inviato la richiesta {msg}")

    for _ in range(5):
        msg = "Preleva"
        conn.send(destination="/queue/requests", body=msg)
        print(f"[CLIENT] Ho inviato la richiesta {msg}")

    for _ in range(1):
        msg = "Svuota"
        conn.send(destination="/queue/requests", body=msg)
        print(f"[CLIENT] Ho inviato la richiesta {msg}")

    conn.disconnect()
