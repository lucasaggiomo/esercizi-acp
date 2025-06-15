import stomp
import time
from typing import Any

from statsListeners import StatsListener, TicketsListener

import multiprocessing as mp

HOST = "localhost"
PORT = 61613

TOPIC_TICKETS = "/topic/tickets"
TOPIC_STATS = "/topic/stats"

DIM_CODA = 5
MAX_LEN_STR = 32


if __name__ == "__main__":

    queue = mp.Queue(maxsize=DIM_CODA)

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
