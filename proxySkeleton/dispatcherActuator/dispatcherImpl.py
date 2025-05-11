from __future__ import annotations
from interface import DispatcherService
from multiprocessing import Queue

DEFAULT_QUEUE_SIZE = 5


class DispatcherImpl(DispatcherService):
    def __init__(self, size=DEFAULT_QUEUE_SIZE):
        self.queue = Queue(size)

    def sendCommand(self, command):
        print(f"[DispatcherImpl] Sending command {command}")
        self.queue.put(command)

    def getCommand(self):
        command = self.queue.get()
        print(f"[DispatcherImpl] Got command {command}")
        return command
