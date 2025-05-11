import sys
import threading as th

import richiestaRisposta as r
import stomp
from utils import getFromArgvOrDefault

NUM_RICHIESTE = 10


class RispostaListener(stomp.ConnectionListener):
    def __init__(self, conn: stomp.Connection, stopEvent: th.Event):
        self.conn = conn
        self.stopEvent = stopEvent

    def on_message(self, frame):
        if frame.body == "STOP":
            print("Ho ricevuto STOP")
            self.stopEvent.set()
            return

        risposta = r.Risposta.parseRisposta(frame.body)
        print(
            f"Il messaggio ricevuto è una risposta di una richiesta di tipo {risposta.tipo}, con messaggio {risposta.data}"
        )


if __name__ == "__main__":
    HOST = getFromArgvOrDefault(1, "127.0.0.1")
    PORT = getFromArgvOrDefault(2, 61613)
    print(f"Host: {HOST}, Port: {PORT}")

    conn = stomp.Connection([(HOST, PORT)])
    conn.connect(wait=True)

    stopEvent = th.Event()

    # si mette in ascolto per le risposte
    conn.set_listener("rispostaListener", RispostaListener(conn, stopEvent))
    conn.subscribe("/topic/stop", 1, "auto")
    conn.subscribe("/queue/risposte", 2, "auto")

    # invia le richieste
    for _ in range(NUM_RICHIESTE):
        richiesta = r.Richiesta.generateRandomRichiesta()
        print(f"Invio la richiesta {richiesta} al dispatcher")
        conn.send("/queue/richieste", str(richiesta))

    stopEvent.wait()

    conn.disconnect()
    sys.exit(0)
