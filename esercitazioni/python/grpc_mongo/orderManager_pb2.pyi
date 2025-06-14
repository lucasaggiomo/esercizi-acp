from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("_id", "items", "descrizione", "prezzo", "destinazione")
    _ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DESCRIZIONE_FIELD_NUMBER: _ClassVar[int]
    PREZZO_FIELD_NUMBER: _ClassVar[int]
    DESTINAZIONE_FIELD_NUMBER: _ClassVar[int]
    _id: str
    items: _containers.RepeatedScalarFieldContainer[str]
    descrizione: str
    prezzo: float
    destinazione: str
    def __init__(self, _id: _Optional[str] = ..., items: _Optional[_Iterable[str]] = ..., descrizione: _Optional[str] = ..., prezzo: _Optional[float] = ..., destinazione: _Optional[str] = ...) -> None: ...

class CombinedShipment(_message.Message):
    __slots__ = ("_id", "stato", "orders", "destinazione")
    _ID_FIELD_NUMBER: _ClassVar[int]
    STATO_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    DESTINAZIONE_FIELD_NUMBER: _ClassVar[int]
    _id: str
    stato: str
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    destinazione: str
    def __init__(self, _id: _Optional[str] = ..., stato: _Optional[str] = ..., orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ..., destinazione: _Optional[str] = ...) -> None: ...

class StringMessage(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...
