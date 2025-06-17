import sys
import threading as th
import time
import stomp
import grpc

import magazzino_pb2 as magazzino
import magazzino_pb2_grpc as magazzino_grpc
from tipoRichiesta import TipoRichiesta

HOST_STOMP = "localhost"
PORT_STOMP = 61613

CODA_RICHIESTA = "/queue/richiesta"

DELIMITER = "-"


def handleRequest(
    conn: stomp.Connection,
    richiesta: str,
    rispostaDest: str,
    stub: magazzino_grpc.MagazzinoServiceStub,
):
    # estrae le informazioni dalla richiesta
    splitted = richiesta.split(DELIMITER)
    try:
        tipo = TipoRichiesta(splitted[0])

        match tipo:
            case TipoRichiesta.DEPOSITA:
                valore = int(splitted[1])

                articolo = magazzino.Articolo(id=valore)
                print(
                    f"    [DISPATCHER] Invio una richiesta di deposito dell'articolo {valore}"
                )
                stringMessage: magazzino.StringMessage = stub.deposita(articolo)
                risposta = stringMessage.value
                print(f"    [DISPATCHER] Ho ricevuto '{risposta}'")

            case TipoRichiesta.PRELEVA:
                empty = magazzino.Empty()
                print(f"    [DISPATCHER] Invio una richiesta di prelievo")
                articolo: magazzino.Articolo = stub.preleva(empty)
                risposta = str(articolo.id)
                print(f"    [DISPATCHER] Ho ricevuto '{risposta}'")

    except ValueError:
        print(f"    [DISPATCHER] Tipo di richiesta non riconosciuto")
        risposta = "Tipo di richiesta non riconosciuto"

    print(f"        [DISPATCHER] Invio la risposta {risposta} al client")
    conn.send(destination=rispostaDest, body=risposta)


class RichiestaListener(stomp.ConnectionListener):
    def __init__(
        self, conn: stomp.Connection, stub: magazzino_grpc.MagazzinoServiceStub
    ):
        super().__init__()
        self.conn = conn
        self.stub = stub

    def on_message(self, frame: stomp.utils.Frame):
        text = frame.body
        rispostaDest = frame.headers["reply-to"]
        print(
            f"[DISPATCHER] Ho ricevuto la richiesta '{text}' a cui rispondere su '{rispostaDest}'"
        )

        thread = th.Thread(
            target=handleRequest, args=(self.conn, text, rispostaDest, self.stub)
        )
        thread.start()


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            HOST_SERVER = "localhost"
            PORT_SERVER = int(sys.argv[1])
        else:
            HOST_SERVER = sys.argv[1]
            PORT_SERVER = int(sys.argv[2])
    except IndexError:
        print(
            "Inserisci il numero di porta del server (default host = 'localhost'), oppure l'indirizzo seguito dal numero di porta"
        )
        sys.exit(1)

    with grpc.insecure_channel(target=f"{HOST_SERVER}:{PORT_SERVER}") as channel:
        stub = magazzino_grpc.MagazzinoServiceStub(channel)

        connSender = stomp.Connection(
            [(HOST_STOMP, PORT_STOMP)], auto_content_length=False
        )
        connSender.connect(wait=True)

        connReceiver = stomp.Connection(
            [(HOST_STOMP, PORT_STOMP)], auto_content_length=False
        )

        listener = RichiestaListener(connSender, stub)
        connReceiver.set_listener("richiestaListener", listener)
        connReceiver.connect(wait=True)
        connReceiver.subscribe(destination=CODA_RICHIESTA, id=1, ack="auto")

        print("[DISPATCHER] In attesa di richieste...")

        while True:
            time.sleep(1)

        connReceiver.disconnect()
