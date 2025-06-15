import stomp
import time
from typing import Any

from statsListeners import StatsListener, TicketsListener
from statsQueue import StatsQueue

import multiprocessing as mp

HOST = "localhost"
PORT = 61613

TOPIC_TICKETS = "/topic/tickets"
TOPIC_STATS = "/topic/stats"

DIM_CODA = 5


if __name__ == "__main__":
    queue = mp.Queue(maxsize=DIM_CODA)
    lock = mp.Lock()
    prodCV = mp.Condition(lock)
    consCV = mp.Condition(lock)

    # NOTE: questo oggetto non è una shared memory, quindi ogni processo ne avrà la sua copia.
    # Tuttavia gli attributi di tale oggetto sono shared memory (queue, lock, prodCV, consCV)
    queue = StatsQueue(queue, lock, prodCV, consCV)

    conn1 = stomp.Connection([(HOST, PORT)], auto_content_length=False)
    statsListener = StatsListener(queue)
    conn1.set_listener("statsListener", statsListener)
    conn1.connect(wait=True)
    conn1.subscribe(destination=TOPIC_STATS, id=1, ack="auto")

    conn2 = stomp.Connection([(HOST, PORT)], auto_content_length=False)
    ticketsListener = TicketsListener(queue)
    conn2.set_listener("ticketsListener", ticketsListener)
    conn2.connect(wait=True)
    conn2.subscribe(destination=TOPIC_TICKETS, id=2, ack="auto")

    print("[STATS] In attesa di messaggi sui topic...")

    while True:
        time.sleep(1)

    conn1.disconnect()
    conn2.disconnect()
