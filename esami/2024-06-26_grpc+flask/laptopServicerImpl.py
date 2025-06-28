import requests

import grpc
import laptopService_pb2 as laptopService
import laptopService_pb2_grpc as laptopService_grpc

from queues.queue import IQueue
from operation import Operation


# implementazione del servizio
class LaptopServicerImpl(laptopService_grpc.LaptopServiceServicer):
    def __init__(self, queue: IQueue, historyManagerUrl: str):
        super().__init__()
        self.queue = queue
        self.historyManagerUrl = historyManagerUrl

    def sendToHistoryServer(self, op: Operation, serial_number: int) -> str:
        message = {"operation": str(op), "serial_number": serial_number}

        print(
            f"[PRODUCT_MANAGER] Invio all'history manager la richiesta POST con body: {message}"
        )
        response = requests.post(self.historyManagerUrl, json=message)

        try:
            response.raise_for_status()
            risposta = response.json()

            print(
                f"      [PRODUCT_MANAGER] Ho ricevuto dall'history manager la risposta: {risposta} con status code {response.status_code}"
            )

            return risposta

        except requests.HTTPError as e:
            print(f"                [PRODUCT_MANAGER] Errore HTTP: {str(e)}")
            return
        except requests.JSONDecodeError:
            print(f"                [PRODUCT_MANAGER] Errore di decodifica json: {str(e)}")
            return

    def buy(
        self, request: laptopService.Empty, context: grpc.ServicerContext
    ) -> laptopService.Laptop:
        print("[PRODUCT_MANAGER] Ho ricevuto una richiesta di acquisto di un laptop")

        serial_number = self.queue.pop()

        # invia una richiesta POST verso l'History Server
        self.sendToHistoryServer(Operation.BUY, serial_number)

        print(f"[PRODUCT_MANAGER] Invio all'utente il laptop {serial_number}")

        laptop = laptopService.Laptop(serial_number=serial_number)

        return laptop

    def sell(
        self, request: laptopService.Laptop, context: grpc.ServicerContext
    ) -> laptopService.Ack:

        serial_number = request.serial_number

        print(
            f"[PRODUCT_MANAGER] Ho ricevuto una richiesta di vendita del laptop {serial_number}"
        )

        self.queue.push(serial_number)

        # invia una richiesta POST verso l'History Server
        self.sendToHistoryServer(Operation.SELL, serial_number)

        print(f"[PRODUCT_MANAGER] Invio all'utente l'ack")

        ack = laptopService.Ack(successful=True)

        return ack
