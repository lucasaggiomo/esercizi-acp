import socket as s
import threading as th
from printerService.printer import IPrinter
from printerService.tipoStampa import TipoStampa

DELIMITER = "?"


def handleRequest(host: str, port: int, pathFile: str, tipoStampa: TipoStampa):
    # si connette al server
    with s.socket(family=s.AF_INET, type=s.SOCK_STREAM) as socket:
        socket.connect((host, port))

        # invia la richiesta
        message = f"{pathFile}{DELIMITER}{str(tipoStampa)}"

        print(f"    [PROXY] Invio il messaggio {message}")
        message = message.encode("utf-8")

        socket.send(message)

        print(f"    [PROXY] Attendo una risposta...")
        response = socket.recv(1024)
        response = response.decode("utf-8")

        print(f"    [PROXY] Ho ricevuto {response}")


class PrinterProxy(IPrinter):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def print(self, pathFile: str, tipoStampa: TipoStampa):

        # delega ad un thread la gestione della richiesta (per non far rimanere bloccato il proxy sulla receive)
        thread = th.Thread(
            target=handleRequest, args=(self.host, self.port, pathFile, tipoStampa)
        )
        thread.start()
