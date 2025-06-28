import grpc

from concurrent import futures

import laptopService_pb2 as laptopService
import laptopService_pb2_grpc as laptopService_grpc

from queues.codaCircolare import CodaCircolare
from queues.codaProdCons import CodaProdCons

from historyService import HistoryService
from servicerImpl import ServicerImpl

HOST_GRPC = "[::]"
PORT_GRPC = 0

DIM_CODA = 5

HOST_HISTORY_SERVER = "localhost"
PORT_HISTORY_SERVER = 5000

if __name__ == "__main__":
    queue = CodaProdCons(CodaCircolare(DIM_CODA))

    historyService = HistoryService(
        f"http://{HOST_HISTORY_SERVER}:{PORT_HISTORY_SERVER}"
    )

    servicer = ServicerImpl(queue, historyService)

    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))

    laptopService_grpc.add_LaptopServiceServicer_to_server(servicer, server)

    PORT_GRPC = server.add_insecure_port(f"{HOST_GRPC}:{PORT_GRPC}")
    server.start()

    print(f"[PRODUCT-MANAGER] In ascolto sulla porta {PORT_GRPC}...")

    server.wait_for_termination()
    server.stop()
