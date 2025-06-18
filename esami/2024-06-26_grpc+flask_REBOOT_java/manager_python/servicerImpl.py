import grpc

import laptopService_pb2 as laptopService
import laptopService_pb2_grpc as laptopService_grpc

from queues.queue import IQueue
from tipoRichiesta import TipoRichiesta
from historyService import HistoryService


class ServicerImpl(laptopService_grpc.LaptopServiceServicer):
    def __init__(self, queue: IQueue, historyService: HistoryService):
        super().__init__()
        self.queue = queue
        self.historyService = historyService

    def buy(
        self, request: laptopService.Empty, context: grpc.ServicerContext
    ) -> laptopService.Laptop:
        print(f"    [SERVICER-BUY] Ho ricevuto una richiesta di acquisto di un laptop")

        serialNumber = self.queue.pop()

        self.historyService.update_history(TipoRichiesta.ACQUISTO, serialNumber)

        print(f"                [SERVICER-BUY] Restituisco il laptop {serialNumber}")

        return laptopService.Laptop(serial_number=serialNumber)

    def sell(
        self, request: laptopService.Laptop, context: grpc.ServicerContext
    ) -> laptopService.StringMessage:

        serialNumber = request.serial_number

        print(
            f"    [SERVICER-SELL] Ho ricevuto una richiesta di vendita del laptop {serialNumber}"
        )

        self.queue.push(serialNumber)

        self.historyService.update_history(TipoRichiesta.VENDITA, serialNumber)

        risposta = "ACK"

        print(f"    [SERVICER-SELL] Restituisco il messaggio {risposta}")

        return laptopService.StringMessage(value=risposta)
