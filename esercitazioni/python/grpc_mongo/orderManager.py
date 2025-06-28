import grpc
from concurrent import futures

import orderManager_pb2 as orderManager
import orderManager_pb2_grpc as orderManager_grpc

from orderManagerServicer import OrderManagerServicerImpl

from mongoService import MongoService

PORT_GRPC = 0

HOST_MONGO = "localhost"
PORT_MONGO = 27017

DB_NAME = "OrderManagementDB"

if __name__ == "__main__":
    mongoService = MongoService(HOST_MONGO, PORT_MONGO)
    db = mongoService.getDatabase(DB_NAME)

    # istanzio il server
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))

    # istanzio il servicer
    servicer = OrderManagerServicerImpl(db)

    orderManager_grpc.add_OrderManagerServiceServicer_to_server(servicer, server)

    PORT_GRPC = server.add_insecure_port(f"[::]:{PORT_GRPC}")

    server.start()

    print(f"[ORDER MANAGER] In ascolto sulla porta {PORT_GRPC}...")

    server.wait_for_termination()

    mongoService.closeConnection()
