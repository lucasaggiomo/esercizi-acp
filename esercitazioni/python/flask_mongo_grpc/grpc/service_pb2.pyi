from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Sensor(_message.Message):
    __slots__ = ("_id", "dataType")
    _ID_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    _id: int
    dataType: str
    def __init__(self, _id: _Optional[int] = ..., dataType: _Optional[str] = ...) -> None: ...

class MeanRequest(_message.Message):
    __slots__ = ("sensor_id", "dataType")
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    sensor_id: int
    dataType: str
    def __init__(self, sensor_id: _Optional[int] = ..., dataType: _Optional[str] = ...) -> None: ...

class StringMessage(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...
