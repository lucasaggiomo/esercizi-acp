import stomp
from stomp.utils import Frame
import threading as th
import random
import sys
import time

from stompService import StompService

HOST_STOMP = "localhost"
PORT_STOMP = 61613

RESPONSE_TOPIC = "/topic/response"
REQUEST_TOPIC = "/topic/request"

NUM_CREATE = 4
NUM_UPDATE = 2


class ResponseListener(stomp.ConnectionListener):
    def __init__(self):
        super().__init__()

    def on_message(self, frame: Frame):
        print("[OPERATOR] Ho ricevuto " + frame.body)


if __name__ == "__main__":
    try:
        operator = sys.argv[1]
    except IndexError:
        print("Inserisci l'username dell'operator")
        sys.exit(1)

    conn = stomp.Connection(host_and_ports=[(HOST_STOMP, PORT_STOMP)])

    # si connette al provider
    conn.connect(wait=True)

    listener = ResponseListener()
    conn.set_listener("listener", listener)

    conn.subscribe(destination=RESPONSE_TOPIC, id=1, ack="auto")

    # crea una connessione differente per le send
    conn2 = stomp.Connection([(HOST_STOMP, PORT_STOMP)])
    conn2.connect(wait=True)

    stompService = StompService(conn2, destination=REQUEST_TOPIC)

    threads: list[th.Thread] = []

    clients = ["Giovanni", "Gianluca", "Gianmario", "Gianni"]
    hotels = [f"{c}'s Hotel" for c in clients]

    print("[OPERATOR] Inizio ad inviare le richieste...")

    for i in range(NUM_CREATE):
        client = random.choice(clients)
        hotel = random.choice(hotels)
        nights = random.randint(1, 5)
        people = random.randint(1, 5)
        cost = 20 + random.random() * 10  # [20, 30]

        t = th.Thread(
            target=stompService.create,
            args=(client, hotel, operator, nights, people, cost),
        )
        threads.append(t)
        t.start()

    for i in range(NUM_UPDATE):
        discount = 10 + random.random() * 10  # [10, 20]
        nights = random.randint(1, 5)
        t = th.Thread(
            target=stompService.update,
            args=(discount, operator, nights),
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    while True:
        time.sleep(60)

    conn.disconnect()
