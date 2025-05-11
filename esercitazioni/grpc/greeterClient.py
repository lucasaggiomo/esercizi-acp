import sys
from typing import Iterable, Iterator

import helloworld_pb2
import helloworld_pb2_grpc

import grpc


def getHelloRequest(name: str):
    return helloworld_pb2.HelloRequest(name=name)


def getHelloRequestGenerator(names: list[str]):
    for name in names:
        yield helloworld_pb2.HelloRequest(name=name)


def sayHello(name: str, stub: helloworld_pb2_grpc.GreeterStub):
    request = getHelloRequest(name)

    print(f"[Client] Invio la richiesta SayHello con nome {request.name}")
    response: helloworld_pb2.HelloReply = stub.SayHello(request)

    print(f"[Client] Ho ricevuto la risposta:\n{response.message}")


def sayHelloToEveryone(names: list[str], stub: helloworld_pb2_grpc.GreeterStub):
    requests = getHelloRequestGenerator(names)

    print(f"[Client] Invio la richiesta SayHelloToEveryone con nomi: {names}")
    response: helloworld_pb2.HelloReply = stub.SayHelloToEveryone(requests)

    print(f"[Client] Ho ricevuto la risposta:\n{response.message}")


def sayManyHello(name: str, stub: helloworld_pb2_grpc.GreeterStub):
    request = getHelloRequest(name)

    print(f"[Client] Invio la richiesta SayManyHello con nome: {name}")
    responses: Iterator[helloworld_pb2.HelloReply] = stub.SayManyHello(request)

    messages = [response.message for response in responses]
    print(f"[Client] Ho ricevuto le risposte:\n{"\n".join(messages)}")


def sayManyHelloToEveryone(names: list[str], stub: helloworld_pb2_grpc.GreeterStub):
    requests = getHelloRequestGenerator(names)

    print(f"[Client] Invio le richieste SayManyHelloToEveryone con nomi: {names}")
    responses: Iterator[helloworld_pb2.HelloReply] = stub.SayManyHelloToEveryone(requests)

    messages = [response.message for response in responses]
    print(f"[Client] Ho ricevuto le risposte:\n{"\n".join(messages)}")


def run(port: int):
    with grpc.insecure_channel(f"localhost:{port}") as channel:

        stub = helloworld_pb2_grpc.GreeterStub(channel)

        sayHello("EXIT", stub)

        # print("-----------------------------------------------")
        # sayHello("Giovanni", stub)

        # print("-----------------------------------------------")
        # sayHelloToEveryone(["Giovanni", "Luca", "Vittorio"], stub)

        # print("-----------------------------------------------")
        # sayManyHello("Giovanni", stub)

        # print("-----------------------------------------------")
        # sayManyHelloToEveryone(["Giovanni", "Luca", "Vittorio"], stub)


if __name__ == "__main__":
    try:
        PORT = sys.argv[1]
    except:
        print("Insert name port as first argument")
        sys.exit(1)

    run(PORT)
