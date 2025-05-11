import multiprocessing as mp
import sys
import time

import magazzino_pb2
import magazzino_pb2_grpc
import stomp
from products import ProductType

import grpc


def handleRequest(
    host: str,
    port: int,
    request: str,
):
    conn = stomp.Connection([("localhost", 61613)])
    conn.connect(wait=True)

    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = magazzino_pb2_grpc.MagazzinoStub(channel)

        stuff = request.split("-")
        if stuff[0] == "Deposita":
            idItem = int(stuff[1])
            articolo = ProductType(stuff[2])
            item = magazzino_pb2.Item(idItem=idItem, type=str(articolo))

            # deposita sul server
            response: magazzino_pb2.StringMessage = stub.deposita(item)

            # invia la risposta al client
            print("[DISPATCHER] Response: ", response.value)
            conn.send("/queue/responses", response.value)

        elif stuff[0] == "Preleva":
            # preleva dal server
            response: magazzino_pb2.Item = stub.preleva(magazzino_pb2.Empty())

            # invia la risposta al client
            print("[DISPATCHER] Response: ", str(response))
            conn.send("/queue/responses", f"{response.idItem}-{str(response.type)}")

        elif stuff[0] == "Svuota":
            for response in stub.svuota(magazzino_pb2.Empty()):
                # invia la risposta al client
                print("[DISPATCHER] Response: ", str(response))
                conn.send("/queue/responses", f"{response.idItem}-{str(response.type)}")

    conn.disconnect()


class RequestListener(stomp.ConnectionListener):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def on_message(self, frame):
        msg: str = frame.body

        print(f"[DISPATCHER] Ho ricevuto {msg}")

        # Start a process to serve the request
        p = mp.Process(target=handleRequest, args=(self.host, self.port, msg))
        p.start()


if __name__ == "__main__":
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else -1
    HOST = sys.argv[2] if len(sys.argv) > 2 else "localhost"

    conn = stomp.Connection([("127.0.0.1", 61613)])
    conn.connect(wait=True)

    conn.subscribe(destination="/queue/requests", id=1, ack="auto")
    conn.set_listener("listener", RequestListener(HOST, PORT))

    while True:
        time.sleep(60)

    conn.disconnect()
