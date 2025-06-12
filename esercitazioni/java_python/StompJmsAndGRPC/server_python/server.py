# Server (Python). Il server è un server gRPC che implementa i metodi di preleva e
# deposita invocati da Dispatcher (ricevuti da Client) per prelevare e depositare
# articoli in una coda. La dimensione della coda è pari a 5. L’accesso alla coda è
# disciplinato attraverso il problema produttore/consumatore.

import multiprocessing as mp
from concurrent import futures

import grpc
import magazzino_pb2 as magazzino
import magazzino_pb2_grpc as magazzino_grpc

DIM_CODA = 5
PORT = 0


# implementazione del servicer
class MagazzinoServicerImpl(magazzino_grpc.MagazzinoServicer):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def deposita(self, request: magazzino.Articolo, context: grpc.ServicerContext):
        print("[SERVER] Deposito l'articolo con id " + str(request.id))
        self.queue.put(request.id)
        print("[SERVER] Ho depositato l'articolo con id " + str(request.id) + ", invio l'ACK...")

        response = magazzino.Acknowledge(message="ACK")
        return response

    def preleva(self, request: magazzino.Empty, context: grpc.ServicerContext):
        print("[SERVER] Prelevo un articolo...")
        id = self.queue.get()
        print("[SERVER] Ho prelevato l'articolo con id " + str(id))

        response = magazzino.Articolo(id=id)
        return response


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    queue = mp.Queue(DIM_CODA)

    servicer = MagazzinoServicerImpl(queue)
    magazzino_grpc.add_MagazzinoServicer_to_server(servicer, server)

    PORT = server.add_insecure_port(f"[::]:{PORT}")

    server.start()

    print(f"[SERVER] Listening on port {PORT}...")

    server.wait_for_termination()
