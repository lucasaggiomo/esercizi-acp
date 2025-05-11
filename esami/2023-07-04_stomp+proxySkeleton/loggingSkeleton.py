import socket as s
import threading as mp

from loggingService import ILogging
from tipoLog import TipoLog

RECV_SIZE = 1024


def produttoreFunction(conn: s.socket, serviceImpl: ILogging):
    msg = conn.recv(RECV_SIZE).decode("utf-8")

    # effettua il parse del messaggio
    splitted = msg.split("-")
    messaggioLog = splitted[0]
    tipo = TipoLog(int(splitted[1]))

    print(f"[SERVER_PRODUTTORE] Invio il messaggio {messaggioLog} di tipo {tipo}")
    # delega all'implementazione l'esecuzione del servizio
    serviceImpl.log(messaggioLog, tipo)

    conn.close()


# classe skeleton che implementa la comunicazione lato server tramite socket per il servizio ILogging
class LoggingSkeleton(ILogging):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def runSkeleton(self):
        socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket.bind((self.host, self.port))

        self.host, self.port = socket.getsockname()
        print(f"[SKELETON] In ascolto all'indirizzo {self.host}:{self.port}")

        socket.listen(5)

        while True:
            conn, clientAddr = socket.accept()
            print(f"[SKELETON] Connesso con {clientAddr}")

            p = mp.Thread(target=produttoreFunction, args=(conn, self))
            p.start()

        socket.close()
