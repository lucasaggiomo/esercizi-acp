import threading as th
from concurrent import futures

import magazzino_pb2
import magazzino_pb2_grpc

import grpc

PORT = 0
QUEUE_SIZE = 5


# implementazione di una coda che gestisce produttore-consumatore per i thread
class ProdConsQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.testa = 0
        self.coda = 0
        self.size = 0
        self.buffer = [None] * capacity

        self.lock = th.Lock()
        self.cv_cons = th.Condition(self.lock)
        self.cv_prod = th.Condition(self.lock)

    def consume(self):
        self.lock.acquire()

        while self.size == 0:
            self.cv_cons.wait()

        item = self.buffer[self.coda]
        self.coda = (self.coda + 1) % self.capacity
        self.size -= 1

        self.cv_prod.notify()

        self.lock.release()

        return item

    def produce(self, item):
        self.lock.acquire()

        while self.size == self.capacity:
            self.cv_prod.wait()

        self.buffer[self.testa] = item
        self.testa = (self.testa + 1) % self.capacity
        self.size += 1

        self.cv_cons.notify()

        self.lock.release()

    def empty(self) -> bool:
        return self.size == 0

    def __len__(self) -> int:
        return self.size


class MagazzinoServicerImpl(magazzino_pb2_grpc.MagazzinoServicer):
    def __init__(self):
        self.queue = ProdConsQueue(QUEUE_SIZE)

        # lock per svuota
        self.depositaLock = th.Lock()
        self.prelevaLock = th.Lock()

    def deposita(self, item: magazzino_pb2.Item, context) -> magazzino_pb2.StringMessage:
        with self.depositaLock:
            self.queue.produce(item)
            print(f"[SERVER] Ho depositato {item.idItem}-{item.type}...")

        return magazzino_pb2.StringMessage(value="deposited")

    def preleva(self, request: magazzino_pb2.Empty, context) -> magazzino_pb2.Item:
        with self.prelevaLock:
            item: magazzino_pb2.Item = self.queue.consume()
            print(f"[SERVER] Ho prelevato {item.idItem}-{item.type}...")

        return item

    def svuota(self, request, context):
        with self.depositaLock:
            with self.prelevaLock:
                while not self.queue.empty():
                    yield self.preleva(request, context)


if __name__ == "__main__":
    servicer = MagazzinoServicerImpl()
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))

    magazzino_pb2_grpc.add_MagazzinoServicer_to_server(servicer, server)

    PORT = server.add_insecure_port(f"[::]:{PORT}")
    print(f"[SERVER] Listening on port: {PORT}...")

    server.start()

    server.wait_for_termination()
