import grpc
import uuid
from pymongo.database import Database
from typing import Iterator

import orderManager_pb2 as orderManager
import orderManager_pb2_grpc as orderManager_grpc

from utils import orderToDict, dictToOrder, shipmentToDict, dictToShipment


class OrderManagerServicerImpl(orderManager_grpc.OrderManagerServiceServicer):
    ORDERS_COLLECTION = "orders"
    SHIPMENTS_COLLECTION = "shipments"

    def __init__(self, db: Database):
        self.db = db

    def addOrder(
        self, request: orderManager.Order, context: grpc.ServicerContext
    ) -> orderManager.StringMessage:
        request._id = str(uuid.uuid1())
        print(f"[ORDER_MANAGER] Aggiungo un ordine (id generato = {request._id})")

        document = orderToDict(request)
        self.db[OrderManagerServicerImpl.ORDERS_COLLECTION].insert_one(document)

        # restituisce l'id dell'ordine generato
        response = orderManager.StringMessage(value=str(request._id))
        return response

    def getOrder(
        self, request: orderManager.StringMessage, context: grpc.ServicerContext
    ) -> orderManager.Order:
        print(f"[ORDER_MANAGER] Cerco l'ordine con id = {request.value}")

        result = self.db[OrderManagerServicerImpl.ORDERS_COLLECTION].find_one(
            {"_id": request.value}
        )

        if result == None:
            print(
                f"[ORDER_MANAGER] Nessun ordine è stato trovato con id pari a {request.value}"
            )
            order = orderManager.Order()
        else:
            order = dictToOrder(**result)

        return order

    def searchOrders(
        self, request: orderManager.StringMessage, context: grpc.ServicerContext
    ) -> Iterator[orderManager.Order]:
        print(f"[ORDER_MANAGER] Cerco gli ordini con item = {request.value}")

        result = self.db[OrderManagerServicerImpl.ORDERS_COLLECTION].find(
            {"items": {"$in": [request.value]}}
        )
        if result == None:
            print(
                f"[ORDER_MANAGER] Nessun ordine è stato trovato con item {request.value} "
            )
            return [orderManager.Order()]
        else:
            for orderDocument in result:
                yield dictToOrder(**orderDocument)

    def processOrders(
        self,
        request_iterator: Iterator[orderManager.Order],
        context: grpc.ServicerContext,
    ) -> Iterator[orderManager.CombinedShipment]:
        print(f"[ORDER_MANAGER] Creo le spedizioni degli ordini richiesti")

        # ad ogni destinazione univoca associa la lista degli ordini che hanno tale destinazione
        orderDestinationMap: dict[str, list[dict[str, str]]] = {}

        count = 0
        for order in request_iterator:
            count += 1
            print(f"[ORDER_MANAGER] Ordine numero " + count)
            # aggiunge al database l'ordine
            documentOrder = orderToDict(order)
            self.db[OrderManagerServicerImpl.ORDERS_COLLECTION].insert_one(
                documentOrder
            )

            orderDestinationMap.setdefault(order.destinazione, []).append(documentOrder)

        print(f"[ORDER_MANAGER] INIZIO A CREARE GLI SHIPMENT")

        for dest, orderList in orderDestinationMap.items():
            # crea uno shipment per ogni destinazione
            shipmentId = str(uuid.uuid1())
            print(
                f"[ORDER_MANAGER] Invio uno shipment verso {dest} con id {shipmentId}"
            )

            documentShipment = {
                "_id": shipmentId,
                "stato": "PROCESSED",
                "orders": orderList,
                "destinazione": dest,
            }
            shipment = dictToShipment(documentShipment)

            # shipment = orderManager.CombinedShipment(
            #     _id=shipmentId,
            #     stato="PROCESSED",
            #     orders=[dictToOrder(order) for order in orderList],
            #     destinazione=dest,
            # )

            # aggiunge al database lo shipment
            self.db[OrderManagerServicerImpl.SHIPMENTS_COLLECTION].insert_one(
                documentShipment
            )

            # yielda lo shipment
            yield shipment

    def cancelShipment(
        self, request: orderManager.StringMessage, context: grpc.ServicerContext
    ) -> orderManager.StringMessage:
        print(f"[ORDER_MANAGER] Cancello la spedizione con id = {request.value}")

        result = self.db[OrderManagerServicerImpl.SHIPMENTS_COLLECTION].delete_one(
            {"_id": request.value}
        )
        if result.deleted_count == 0:
            print(
                f"[ORDER_MANAGER] Nessuno shipment è stato trovato con id pari a {request.value}"
            )
            return orderManager.StringMessage(value="NOT_FOUND")
        else:
            return orderManager.StringMessage(value="DELETED")
