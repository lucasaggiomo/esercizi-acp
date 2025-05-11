import sys
import threading as th

import stomp


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(counter=0)
def getFromArgvOrDefault(default, type: type = str):
    getFromArgvOrDefault.counter += 1
    index = getFromArgvOrDefault.counter
    if len(sys.argv) > index:
        return type(sys.argv[index])
    return default


class GiovanniListener(stomp.ConnectionListener):
    def __init__(self, conn: stomp.Connection, stopEvent: th.Event):
        self.conn = conn
        self.stopEvent = stopEvent

    def on_message(self, frame):
        print(f"Aggiu ricevut o frame cu messagg: {frame.body}")
        if frame.body == "STOP":
            self.stopEvent.set()


if __name__ == "__main__":
    ADDRESS = getFromArgvOrDefault("127.0.0.1")
    PORT = getFromArgvOrDefault(61613, int)
    print(f"Address: {ADDRESS}, Port: {PORT}")

    conn = stomp.Connection([(ADDRESS, PORT)])
    conn.connect(wait=True)

    stopEvent = th.Event()

    conn.set_listener("giovanniListener", GiovanniListener(conn, stopEvent))
    conn.subscribe("/queue/giovanni", 1, "auto")
    conn.subscribe("/topic/stop", 2, "auto")

    stopEvent.wait()

    conn.disconnect()
    sys.exit(0)
