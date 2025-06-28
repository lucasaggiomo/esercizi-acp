import random
import sys
import time

import stomp
from client_listener import ClientListener
from richiesta import Richiesta

HOST = "localhost"
PORT = 61613

CODA_RISPOSTA = "/queue/risposta"
CODA_RICHIESTA = "/queue/richiesta"
DELIMITER = "-"

if __name__ == "__main__":
    try:
        NUM_RICHIESTE = int(sys.argv[1])
    except IndexError:
        print("Inserisci il numero di richieste da effettuare")
        sys.exit(1)

    conn = stomp.Connection([(HOST, PORT)], auto_content_length=False)

    conn.connect(wait=True)

    listener = ClientListener()
    conn.set_listener("listener", listener)

    conn.subscribe(destination=CODA_RISPOSTA, id=1)

    for i in range(NUM_RICHIESTE):
        messaggio = ""

        if i % 2 == 0:
            richiesta = Richiesta.DEPOSITA
            id_articolo = random.randint(1, 100)
            messaggio = f"{richiesta}{DELIMITER}{id_articolo}"
        else:
            richiesta = Richiesta.PRELEVA
            messaggio = f"{richiesta}"

        print(f"[CLIENT] Invio il messaggio {messaggio}")
        conn.send(destination=CODA_RICHIESTA, body=messaggio, headers={"reply-to": CODA_RISPOSTA})

    while True:
        time.sleep(60)
