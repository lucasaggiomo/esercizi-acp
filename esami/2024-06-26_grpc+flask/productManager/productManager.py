import grpc
from concurrent import futures

from laptopServicerImpl import LaptopServicerImpl
import laptopService_pb2_grpc as laptopService_grpc
from queues.circularQueue import CircularQueue
from queues.prodConsQueue import ProdConsQueue

DIM_CODA = 5
PORT = 0
HISTORY_MANAGER_URL = "http://127.0.0.1:5000"

if __name__ == "__main__":
    # istanzia la coda prod cons
    queue = ProdConsQueue(CircularQueue(capacity=DIM_CODA))

    # istanzia il server
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    servicer = LaptopServicerImpl(queue, HISTORY_MANAGER_URL)

    # aggiunge il servizio al server
    laptopService_grpc.add_LaptopServiceServicer_to_server(servicer, server)

    PORT = server.add_insecure_port(f"[::]:{PORT}")

    # avvia il server
    server.start()

    print(f"[PRODUCT_MANAGER] In ascolto sulla porta {PORT}...")

    # attende la terminazione del server
    server.wait_for_termination()
