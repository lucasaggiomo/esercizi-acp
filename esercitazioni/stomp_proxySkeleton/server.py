import multiprocessing as mp
import socket as s

import richiestaRisposta as r
from service import Service
from utils import getFromArgvOrDefault

RECV_SIZE = 1024


def processFunction(conn: s.socket, service: Service):
    # si mette in ascolto di richieste
    print(f"Attendo un messaggio...")
    msg = conn.recv(RECV_SIZE)
    msg = msg.decode("utf-8")

    print(f"Ho ricevuto un messaggio: {msg}")

    # delega la richiesta al servizio
    richiesta = r.Richiesta.parseRichiesta(msg)
    match richiesta.tipo:
        case r.TipoRichiesta.PRELEVA:
            result = service.preleva()
        case r.TipoRichiesta.DEPOSITA:
            result = service.deposita(richiesta.id)

    # invia una risposta
    risposta = r.Risposta(tipo=richiesta.tipo, data=str(result))
    print(f"Invio la risposta {risposta}")

    conn.send(str(risposta).encode("utf-8"))

    # chiude la connessione TCP
    conn.close()


class ServiceSkeleton(Service):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def runSkeleton(self):
        socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket.bind((self.host, self.port))

        self.host, self.port = socket.getsockname()

        socket.listen(5)

        print(f"Sono in ascolto all'indirizzo {self.host}:{self.port}...")

        processes: list[mp.Process] = []
        while True:
            conn, addr = socket.accept()

            print(f"Connesso con {addr}")

            p = mp.Process(target=processFunction, args=(conn, self))
            p.start()

            processes.append(p)

        # codice non raggiungibile
        print("Aspetto la terminazione dei processi...")
        for p in processes:
            p.join()

        socket.close()


# implementa il servizio
class ServiceImpl(ServiceSkeleton):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.queue = mp.Queue(maxsize=5)

    def preleva(self) -> int:
        id = self.queue.get()
        print(f"PRELIEVO DI {id} EFFETTUATO")
        return id

    def deposita(self, id: int) -> str:
        print(f"DEPOSITO DI {id} EFFETTUATO")
        self.queue.put(id)
        return "depositato"


if __name__ == "__main__":
    HOST = getFromArgvOrDefault(1, "127.0.0.1")
    PORT = getFromArgvOrDefault(2, 0)

    service = ServiceImpl(HOST, PORT)
    service.runSkeleton()
