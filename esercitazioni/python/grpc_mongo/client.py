# Client: genera 5 ordini, e ne richiede l’aggiunta al Manager attraverso addOrder. Per ogni
# invocazione di addOrder, il client stampa a video l’id ottenuto, e verifica l’aggiunta dell’ordine
# attraverso la getOrder, stampando a video i dati dell’ordine.Successivamente, il client richiede la ricerca di un particolare item aggiunto ad uno degli ordini
# precedentemente inviati al Manager, stampando la lista di ordini che contiene quell’item.
# Il Client crea poi 4 ordini, due dei quali hanno la stessa destinazione, e richiede al Manager la
# creazione delle relative spedizioni attraverso la processOrders, stampando a video le informazioni
# sulle spedizioni.
# Infine, il Client richiede la cancellazione di una delle spedizioni attraverso la cancelShipment,
# stampando a video la risposta ottenuta.

import grpc
import sys
from typing import Iterator

import orderManager_pb2 as orderManager
import orderManager_pb2_grpc as orderManager_grpc

from utils import orderToStr, shipmentToStr


def generate_orders_for_processing():

    print("Generating orders to delivery...")

    ord1 = orderManager_grpc.Order(
        prezzo=2332,
        items=["Item - A", "Item - B"],
        descrizione="Updated desc",
        destinazione="San Jose, CA",
    )

    ord2 = orderManager_grpc.Order(
        prezzo=3000, descrizione="Updated desc", destinazione="San Francisco, CA"
    )

    ord3 = orderManager_grpc.Order(
        prezzo=2560, descrizione="Updated desc", destinazione="San Francisco, CA"
    )

    ord4 = orderManager_grpc.Order(
        prezzo=2560, descrizione="Updated desc", destinazione="Mountain View, CA"
    )

    orderList = []
    orderList.append(ord1)
    orderList.append(ord2)
    orderList.append(ord3)
    orderList.append(ord4)

    for processing_orders in orderList:
        yield processing_orders


def orderEquals(order1: orderManager.Order, order2: orderManager.Order) -> bool:
    if (
        order1._id != order2._id
        or order1.descrizione != order2.descrizione
        or order1.prezzo != order2.prezzo
        or order1.destinazione != order2.destinazione
        or order1.items != order2.items
    ):
        return False
    return True


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            PORT = int(sys.argv[1])
            HOST = "localhost"
        else:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
    except IndexError:
        print(
            "Inserisci solo il numero di porta (default host = 'localhost')\ oppure l'indirizzo dell'host seguito dal numero di porta"
        )
        sys.exit(1)

    # si connette a grpc
    with grpc.insecure_channel(target=f"{HOST}:{PORT}") as channel:
        print(f"[CLIENT] Connected to {HOST}:{PORT}")
        # istanzia uno stub associato al channel
        stub = orderManager_grpc.OrderManagerServiceStub(channel)

        items: list[str] = [
            "Item - A",
            "Item - B",
            "Item - C",
            "Item - D",
            "Item - E",
            "Item - F",
            "Item - G",
        ]

        # crea una lista di 5 ordini
        orders: list[orderManager.Order] = []

        orders.append(
            orderManager.Order(
                prezzo=2450.50,
                items=["Item - A", "Item - B", "Item - C"],
                descrizione="This is a Sample order - 1 : descrizione.",
                destinazione="San Jose, CA",
            )
        )

        orders.append(
            orderManager.Order(
                prezzo=1000,
                items=["Item - A", "Item - B"],
                descrizione="Sample order descrizione.",
                destinazione="Naples",
            )
        )

        orders.append(
            orderManager.Order(
                prezzo=1000,
                items=["Item - C"],
                descrizione="Sample order descrizione.",
                destinazione="Rome",
            )
        )

        orders.append(
            orderManager.Order(
                prezzo=1000,
                items=["Item - A", "Item - E"],
                descrizione="Sample order descrizione.",
                destinazione="Milan",
            )
        )

        orders.append(
            orderManager.Order(
                prezzo=1000,
                items=["Item - F", "Item - G"],
                descrizione="Sample order descrizione.",
            )
        )

        for order in orders:
            # aggiunge gli ordini
            print("---------")
            print(f"[CLIENT] Provo ad aggiungere l'ordine seguente:")
            print(orderToStr(order))
            orderID: orderManager.StringMessage = stub.addOrder(order)

            print(
                f"[CLIENT] Ho aggiunto l'ordine con id pari a {orderID.value}, lo verifico con getOrder"
            )
            order._id = orderID.value

            orderID = orderManager.StringMessage(value=orderID.value)
            # verifica l’aggiunta dell’ordine
            orderGot = stub.getOrder(orderID)
            print("Ho ottenuto l'ordine seguente:")
            print(orderToStr(orderGot))

            # confronta gli ordini
            if orderEquals(order, orderGot):
                print(
                    "[CLIENT] Ho confermato che l'ordine è stato aggiunto correttamente"
                )
            else:
                print(
                    "[CLIENT] L'ordine ricevuto è diverso da quello che ho richiesto di aggiungere!"
                )

        print("############")

        for item in items:
            print(f"[CLIENT] Cerco tutti gli ordini che contengono l'item: {item}")
            # ottiene gli ordini che hanno item
            message = orderManager.StringMessage(value=item)
            orderList: Iterator[orderManager.Order] = stub.searchOrders(message)
            print(f"[CLIENT] Gli ordini che contengono l'item {item} sono:")
            for order in orderList:
                print("\t\t" + orderToStr(order))

        print("############")
        proc_order_iterator = generate_orders_for_processing()

        shipments: Iterator[orderManager.CombinedShipment] = stub.processOrders(
            proc_order_iterator
        )
        print(
            "[CLIENT] Ho costruito gli shipment in base alle destinazioni (di alcuni ordini...):"
        )
        for shipment in shipments:
            print("Shipment : ", shipmentToStr(shipment))

        id_shipment_to_delete = shipment._id

        resp: orderManager.StringMessage = stub.cancelShipment(
            order_management_pb2.StringMessage(value=id_shipment_to_delete)
        )
        print("cancelShipment() response: ", resp.value)
