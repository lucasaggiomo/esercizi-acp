import sys
import threading as th
from typing import TypeVar

import stomp

T = TypeVar("T")


def getFromArgvOrDefault(index: int, default: T):
    cast_type = type(default)
    if len(sys.argv) > index:
        return cast_type(sys.argv[index])
    return default


class StopperListener(stomp.ConnectionListener):
    def __init__(self, stopEvent: th.Event):
        self.stopEvent = stopEvent

    def on_message(self, frame):
        print(f"StopperListener: {frame.body}")
        if frame.body == "STOP":
            self.stopEvent.set()
