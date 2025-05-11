import socket

from IMagazzino import IMagazzino
from articolo import Articolo
from operation import Operation
from parser import generateCommand

BUFF_SIZE = 1024


class MagazzinoProxy(IMagazzino):

    def __init__(self, address: str, port: int, timeout: int):
        self.address = address
        self.port = port
        self.timeout = timeout

    def preleva(self, articolo: Articolo) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)

        s.connect((self.address, self.port))
        port = s.getsockname()[1]

        message = generateCommand(Operation.PRELEVA, articolo)

        print(f"[PROXY - {port}] Mando: {message}")

        s.send(message.encode("utf-8"))

        try:
            id_prelievo = int(s.recv(BUFF_SIZE).decode("utf-8"))
        except socket.timeout:
            print(f"[PROXY - {port}] Timeout: nessuna risposta dal server")
            return -1

        print(f"[PROXY - {port}] Ho prelevato l'articolo con id: {id_prelievo}")

        return id_prelievo

    def deposita(self, articolo: Articolo, id: int) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)

        s.connect((self.address, self.port))
        port = s.getsockname()[1]

        message = generateCommand(Operation.DEPOSITA, articolo, id)

        print(f"[PROXY - {port}] Mando: {message}")

        s.send(message.encode("utf-8"))

        try:
            ack = s.recv(BUFF_SIZE).decode("utf-8")
        except socket.timeout:
            print(f"[PROXY - {port}] Timeout: nessuna risposta dal server")
            return -1

        print(f"[PROXY - {port}] Ho ricevuto l'ACK del deposito ({ack})")
