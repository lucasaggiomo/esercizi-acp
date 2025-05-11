from abc import ABC
import threading as th
import socket
import time

from IMagazzino import IMagazzino
from articolo import Articolo
from operation import Operation
from parser import parseCommand

BUFF_SIZE = 1024


def threadFunction(conn: socket.socket, magazzino: IMagazzino):
    command = conn.recv(BUFF_SIZE).decode("utf-8")
    print(f"[SKELETON] Ho ricevuto {command}")

    operation, articolo, id = parseCommand(command)

    match operation:
        case Operation.DEPOSITA:
            print(
                f"[SKELETON - {th.current_thread().name}] Deposito {(articolo.value, id)} nel magazzino, quindi invio l'ACK al cliente..."
            )

            magazzino.deposita(articolo, id)

            time.sleep(1)

            print(f"[SKELETON - {th.current_thread().name}] Invio l'ACK")

            conn.send("ACK".encode("utf-8"))

        case Operation.PRELEVA:
            print(
                f"[SKELETON - {th.current_thread().name}] Prelevo {articolo.value} nel magazzino, quindi invio l'id al cliente..."
            )

            id = magazzino.preleva(articolo)

            time.sleep(1)

            print(f"[SKELETON - {th.current_thread().name}] Invio l'id {id}")

            conn.send(str(id).encode("utf-8"))

    conn.close()


class MagazzinoSkeleton(IMagazzino, ABC):

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

    def runSkeleton(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))

        self.address, self.port = s.getsockname()

        s.listen(5)

        print(f"[SKELETON] Sono in ascolto all'indirizzo {self.address}:{self.port}...")

        threads: list[th.Thread] = []

        try:
            while True:
                conn, addr = s.accept()

                print(f"[SKELETON] Connesso con {addr}")

                t = th.Thread(target=threadFunction, args=(conn, self))
                t.start()

                threads.append(t)

        except KeyboardInterrupt:
            print("[SKELETON] Non sono più in ascolto")

        print("[SKELETON] Attendo la terminazione dei thread creati...")

        for t in threads:
            t.join()

        s.close()
