import random
import time

import stomp

from clientListener import ClientListener
from metodi import Metodo

HOST = "localhost"
PORT = 61613

CODA_RISPOSTA = "/queue/risposta"
CODA_RICHIESTA = "/queue/richiesta"
DELIMITER = "-"

if __name__ == "__main__":

    conn = stomp.Connection([(HOST, PORT)], auto_content_length=False)

    conn.connect(wait=True)

    listener = ClientListener()
    conn.subscribe(CODA_RISPOSTA, "1", "auto")

    conn.set_listener("", listener)

    for i in range(10):
        messaggio = ""

        if i % 2 == 0:
            # preleva
            metodo = Metodo.PRELEVA
            messaggio = f"{metodo}"

        else:
            # deposita
            metodo = Metodo.DEPOSITA
            IDArticolo = random.randint(1, 100)
            messaggio = f"{metodo}{DELIMITER}{IDArticolo}"

        print("[CLIENT] Invio la richiesta seguente: " + messaggio)
        conn.send(CODA_RICHIESTA, messaggio, headers={"reply-to": CODA_RISPOSTA})

    while True:
        time.sleep(60)
