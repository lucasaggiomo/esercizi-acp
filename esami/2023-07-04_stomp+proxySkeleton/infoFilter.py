import time
from datetime import datetime
from typing import Callable

import stomp
from tipoLog import TipoLog

STOMP_HOST = "localhost"
STOMP_PORT = 61613


class InfoListener(stomp.ConnectionListener):
    def __init__(self, logCallback: Callable[[str], None]):
        """
        **logCallback** è la funzione di notifica che viene eseguita ad ogni messaggio di tipo *TipoLog.INFO* ricevuto
        """
        self.logCallback = logCallback

    def on_message(self, frame):
        msg: str = frame.body

        splitted = msg.split("-")
        messaggioLog = splitted[0]
        tipo = TipoLog(int(splitted[1]))

        if tipo == TipoLog.INFO:
            self.logCallback(messaggioLog)


def logCallback(messaggioLog: str):
    print(f"[INFO_FILTER] {datetime.now()} - {messaggioLog}")
    with open("info.txt", mode="a") as infoFile:
        infoFile.write(f"{datetime.now()} - {messaggioLog}\n")


if __name__ == "__main__":
    conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)])
    conn.connect(wait=True)

    conn.set_listener("infoListener", InfoListener(logCallback))
    conn.subscribe("/queue/info", id=1, ack="auto")

    print(f"[INFO_FILTER] Sono in ascolto di messaggi di tipo {TipoLog.INFO}...")

    while True:
        time.sleep(60)

    conn.disconnect()
