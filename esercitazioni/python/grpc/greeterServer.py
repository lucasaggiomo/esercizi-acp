import random
from concurrent import futures
from typing import Callable, Iterable

import helloworld_pb2
import helloworld_pb2_grpc

import grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request: helloworld_pb2.HelloRequest, context):
        print(
            f"[Server] SayHello method invoked with request name {request.name}, returning response..."
        )
        return helloworld_pb2.HelloReply(message=f"Hello {request.name}")

    def SayHelloToEveryone(self, request_iterator: Iterable[helloworld_pb2.HelloRequest], context):
        names = list(map(lambda req: req.name, request_iterator))
        print(
            f"[Server] SayHelloToEveryone method invoked with request names {names}, returning response..."
        )
        message = f"Hello {", ".join(names)}"
        return helloworld_pb2.HelloReply(message=message)

    def SayManyHello(self, request: helloworld_pb2.HelloRequest, context):
        times = random.randint(1, 5)
        print(
            f"[Server] SayManyHello method invoked with request name {request.name}, returning {times} responses..."
        )
        for _ in range(times):
            yield helloworld_pb2.HelloReply(message=f"Hello {request.name}")

    def SayManyHelloToEveryone(
        self, request_iterator: Iterable[helloworld_pb2.HelloRequest], context
    ):
        times = random.randint(1, 5)
        names = list(map(lambda req: req.name, request_iterator))
        print(
            f"[Server] SayManyHelloToEveryone method invoked with request names {names}, returning {times} responses..."
        )
        message = f"Hello {", ".join(names)}"
        for _ in range(times):
            yield helloworld_pb2.HelloReply(message=message)


def run():
    port = 0

    servicer = Greeter()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    helloworld_pb2_grpc.add_GreeterServicer_to_server(servicer, server)

    port = server.add_insecure_port(f"[::]:{port}")
    print(f"Server listening on port: {port}...")

    server.start()

    server.wait_for_termination()


if __name__ == "__main__":
    run()
