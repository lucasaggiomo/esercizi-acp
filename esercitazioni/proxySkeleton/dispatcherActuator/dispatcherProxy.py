import socket
import time

from interface import DispatcherService
from parser import SEND_CMD, GET_CMD

BUFF_SIZE = 1024


class DispatcherProxy(DispatcherService):
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def sendCommand(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))

        message = SEND_CMD + "#" + str((command))

        print(f"[PROXY] Mando: {message}")
        time.sleep(1)
        s.send(message.encode("utf-8"))

        message = s.recv(BUFF_SIZE).decode("utf-8")

        print(f"[PROXY] Ho ricevuto: {message}")

        s.close()

    def getCommand(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))

        message = GET_CMD + "#"

        print(f"[PROXY] Mando: {message}")
        time.sleep(1)
        s.send(message.encode("utf-8"))

        data = int(s.recv(BUFF_SIZE).decode("utf-8"))

        print(f"[PROXY] Ho ricevuto: {data}")

        s.close()

        return data
