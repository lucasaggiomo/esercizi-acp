import socket as s
import multiprocessing as mp

from printerService.printer import IPrinter
from printerService.tipoStampa import TipoStampa

DELIMITER = "?"


def processFunction(socket: s.socket, printerService: IPrinter):
    # preleva gli input dalla socket
    data = socket.recv(1024)
    data = data.decode("utf-8")

    print(f"     [PROCESS_FUN] Ricevuto il messaggio {data}")

    splitted = data.split(DELIMITER)
    pathFile = splitted[0]

    response = ""

    try:
        tipoStampa = TipoStampa(splitted[1])
        printerService.print(pathFile, tipoStampa)
        response = "ACK"

    except ValueError:
        print(f"        [PROCESS_FUN] Tipo di stampa non riconosciuto")
        response = "Tipo di stampa non riconosciuto"

    except Exception as e:
        print(f"        [PROCESS_FUN] Eccezione inaspettata: {e}")
        response = "Errore interno"

    finally:
        response = response.encode("utf-8")
        socket.send(response)
        socket.close()


class PrinterSkeleton(IPrinter):
    def __init__(self, host: str, port: int, printerService: IPrinter):
        self.host = host
        self.port = port
        self.printerService = printerService

    def print(self, pathFile: str, tipoStampa: TipoStampa):
        # delega la richiesta al servizio reale
        self.printerService.print(pathFile, tipoStampa)

    def runSkeleton(self):
        with s.socket(family=s.AF_INET, type=s.SOCK_STREAM) as socket:
            socket.bind((self.host, self.port))

            self.host, self.port = socket.getsockname()

            print(f"[SKELETON] In ascolto all'indirizzo {self.host}:{self.port}...")

            socket.listen(5)

            while True:
                clientSocket, clientAddr = socket.accept()

                print(f"[SKELETON] Connesso con {clientAddr[0]}:{clientAddr[1]}")

                process = mp.Process(
                    target=processFunction,
                    args=(
                        clientSocket,
                        self,
                    ),
                )
                process.start()
