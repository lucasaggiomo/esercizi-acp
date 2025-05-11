from interface import DispatcherService
import socket
from multiprocessing import Process
from parser import SEND_CMD, GET_CMD

BUFF_SIZE = 1024


def procFunction(conn: socket.socket, service: DispatcherService):
    data = conn.recv(BUFF_SIZE)
    message = data.decode("utf-8")

    print(f"[DispatcherSkeleton prodFunction] MESSAGE received: {message}")

    # assumiamo un protocollo del tipo:
    # SENDorGET#COMANDO

    # Nota: la logica di parsing andrebbe separata dalla logica di comunicazione
    request = message.split("#")
    command = request[0]

    if command == SEND_CMD:
        value_to_send = int(request[1])
        print(
            f"[DispatcherSkeleton prodFunction] request is {SEND_CMD}, value is: {value_to_send}"
        )
        service.sendCommand(value_to_send)
        result = "ACK"

    elif command == GET_CMD:
        print(
            f"[DispatcherSkeleton prodFunction] request is {GET_CMD}... wait for result"
        )
        result = service.getCommand()

    print(f"[DispatcherSkeleton prodFunction] result to send back: {result}")

    conn.send(str(result).encode("utf-8"))

    conn.close()


class DispatcherSkel(DispatcherService):
    def __init__(self, address, port, service: DispatcherService):
        self.address = address
        self.port = port
        self.service = service

    def sendCommand(self, command):
        self.service.sendCommand(command)

    def getCommand(self):
        return self.service.getCommand()

    def runSkeleton(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        s.listen(5)

        while True:
            print("[DispatcherSkeleton] Aspetto una nuova connessione...")

            conn, addr = s.accept()

            print(f"[DispatcherSkeleton] Nuova connessione con {(conn, addr)}")

            p = Process(target=procFunction, args=(conn, self.service))
            p.start()

        s.close()
        print("[DispatcherSkeleton] socket is closed...")
