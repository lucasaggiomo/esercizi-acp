import multiprocessing as mp
import socket as s
import sys
import threading as th

import richiestaRisposta as r
import stomp
from service import Service
from utils import StopperListener, getFromArgvOrDefault

NUM_RICHIESTE = 10

RECV_SIZE = 1024


# classe proxy che implementa l'interfaccia Service lato client, gestendo la comunicazione con il server
class ServiceProxy(Service):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def sendMessageAndWaitResponse(self, msg: str) -> str:
        socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket.connect((self.host, self.port))

        print(f"[PROXY] Mando il messaggio {msg}")
        socket.send(msg.encode("utf-8"))

        msg = socket.recv(RECV_SIZE).decode("utf-8")
        print(f"[PROXY] Ho ricevuto la risposta {msg}")

        socket.close()

        return msg

    def preleva(self) -> int:
        richiesta = r.Richiesta(r.TipoRichiesta.PRELEVA)
        msg = self.sendMessageAndWaitResponse(str(richiesta))
        risposta = r.Risposta.parseRisposta(msg)
        return int(risposta.data)

    def deposita(self, id: int) -> str:
        richiesta = r.Richiesta(r.TipoRichiesta.DEPOSITA, id)
        msg = self.sendMessageAndWaitResponse(str(richiesta))
        risposta = r.Risposta.parseRisposta(msg)
        return risposta.data


def processFunction(proxy: ServiceProxy, richiesta: r.Richiesta, HOST_STOMP, PORT_STOMP):
    # inoltra la richiesta al server attraverso il proxy
    # NOTA: con questo approccio il Proxy rigenera nuovamente la richiesta inutilmente, però è
    # più flessibile qualora la comunicazione tra dispatcher e server necessiti un altro tipo di formulazione della richiesta
    match richiesta.tipo:
        case r.TipoRichiesta.PRELEVA:
            print("Prelevo dal proxy...")
            result = proxy.preleva()
            print(f"Ho ricevuto {result}")
        case r.TipoRichiesta.DEPOSITA:
            print(f"Deposito {richiesta.id} nel proxy...")
            result = proxy.deposita(richiesta.id)
            print(f"Ho ricevuto {result}")

    # genera la risposta
    risposta = r.Risposta(tipo=richiesta.tipo, data=str(result))

    # si connette al provider ed invia la risposta
    conn = stomp.Connection([(HOST_STOMP, PORT_STOMP)])
    conn.connect(wait=True)

    conn.send("/queue/risposte", str(risposta))


class RichiestaListener(stomp.ConnectionListener):
    def __init__(
        self,
        conn: stomp.Connection,
        host_server: str,
        port_server: int,
        stopEvent: th.Event,
        host_stomp: str,
        port_stomp: int,
    ):
        self.conn = conn
        self.host_server = host_server
        self.port_server = port_server
        self.stopEvent = stopEvent
        self.host_stomp = host_stomp
        self.port_stomp = port_stomp
        self.processes: list[mp.Process] = []

    def on_message(self, frame):
        if frame.body == "STOP":
            print("Ho ricevuto STOP")

            print("Attendo che tutti i processi creati terminino...")
            for p in self.processes:
                p.join()

            self.stopEvent.set()

            return

        # print(f"Ho ricevuto {frame.body}")
        # Generate the Proxy
        richiesta = r.Richiesta.parseRichiesta(frame.body)
        print(
            f"Il messaggio ricevuto è una richiesta di tipo {richiesta.tipo} con id {richiesta.id}"
        )

        proxy = ServiceProxy(self.host_server, self.port_server)

        # delega ad un nuovo processo la gestione della richiesta
        p = mp.Process(
            target=processFunction, args=(proxy, richiesta, self.host_stomp, self.port_stomp)
        )
        self.processes.append(p)
        p.start()


if __name__ == "__main__":
    PORT_SERVER = getFromArgvOrDefault(1, -1)
    HOST_SERVER = getFromArgvOrDefault(2, "127.0.0.1")

    HOST_STOMP = getFromArgvOrDefault(3, "127.0.0.1")
    PORT_STOMP = getFromArgvOrDefault(4, 61613)

    conn = stomp.Connection([(HOST_STOMP, PORT_STOMP)])
    conn.connect(wait=True)

    stopEvent = th.Event()

    # si mette in ascolto per le richieste
    conn.set_listener(
        "richiestaListener",
        RichiestaListener(conn, HOST_SERVER, PORT_SERVER, stopEvent, HOST_STOMP, PORT_STOMP),
    )
    conn.subscribe("/topic/stop", 1, "auto")
    conn.subscribe("/queue/richieste", 2, "auto")

    stopEvent.wait()

    conn.disconnect()
    sys.exit(0)
