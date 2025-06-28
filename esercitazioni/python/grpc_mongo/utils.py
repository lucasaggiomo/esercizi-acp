import orderManager_pb2 as orderManager
import orderManager_pb2_grpc as orderManager_grpc
from typing import Any


def dictToOrder(**kwargs) -> orderManager.Order:
    # utilizza operatore di unpacking
    return orderManager.Order(**kwargs)
    # return orderManager.Order(
    #     _id=kwargs["_id"],
    #     items=kwargs["items"],
    #     descrizione=kwargs["descrizione"],
    #     prezzo=kwargs["prezzo"],
    #     destinazione=kwargs["destinazione"],
    # )


def orderToDict(order: orderManager.Order) -> dict[str, Any]:
    return {
        "_id": order._id,
        "items": [] if order.items is None else list(order.items),
        "descrizione": order.descrizione,
        "prezzo": order.prezzo,
        "destinazione": order.destinazione,
    }


def dictToShipment(**kwargs) -> orderManager.CombinedShipment:
    # utilizza operatore di unpacking
    # return orderManager.CombinedShipment(**kwargs)
    return orderManager.Order(
        _id=kwargs["_id"],
        stato=kwargs["stato"],
        orders=[dictToOrder(order) for order in kwargs["orders"]],
        destinazione=kwargs["destinazione"],
    )


def shipmentToDict(shipment: orderManager.CombinedShipment) -> dict[str, Any]:
    return {
        "_id": shipment._id,
        "stato": shipment.stato,
        "orders": [orderToDict(order) for order in shipment.orders],
        "destinazione": shipment.destinazione,
    }


def orderToStr(order: orderManager.Order) -> str:
    return str(orderToDict(order))


def shipmentToStr(shipment: orderManager.CombinedShipment) -> str:
    return str(shipmentToDict(shipment))
