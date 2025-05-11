import sys
import time
from datetime import datetime
from typing import Callable

import stomp
from tipoLog import TipoLog

STOMP_HOST = "localhost"
STOMP_PORT = 61613

MESSAGES = ["fatal", "exception"]


class ErrorListener(stomp.ConnectionListener):
    def __init__(self, message: str, logCallback: Callable[[str], None]):
        """
        **message** è il messaggio da dover leggere\n
        **logCallback** è la funzione di notifica che viene eseguita ad ogni *message* ricevuto
        """
        self.message = message
        self.logCallback = logCallback

    def on_message(self, frame):
        msg: str = frame.body

        splitted = msg.split("-")
        messaggioLog = splitted[0]
        # tipo = TipoLog(int(splitted[1]))

        if messaggioLog == self.message:
            self.logCallback(messaggioLog)


def logCallback(messaggioLog: str):
    print(f"[ERROR_CHECKER] {datetime.now()} - {messaggioLog}")
    with open("error.txt", mode="a") as errorFile:
        errorFile.write(f"{datetime.now()} - {messaggioLog}\n")


if __name__ == "__main__":
    try:
        MESSAGE = sys.argv[1]
        if MESSAGE not in MESSAGES:
            print("Il messaggio di errore può essere uno tra i seguenti:")
            print("\n".join(MESSAGES))
    except IndexError:
        print("Inserisci il messaggio di errore da voler notificare, uno tra i seguenti")
        print("\n".join(MESSAGES))
        sys.exit(1)

    conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)])
    conn.connect(wait=True)

    conn.set_listener("errorListener", ErrorListener(MESSAGE, logCallback))
    conn.subscribe("/queue/error", id=1, ack="auto")

    print(f"[ERROR_CHECKER] Sono in ascolto di errori con messaggio {MESSAGE}...")

    while True:
        time.sleep(60)

    conn.disconnect()
