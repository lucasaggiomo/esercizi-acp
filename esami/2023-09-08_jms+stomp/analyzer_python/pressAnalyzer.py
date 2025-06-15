import threading as th
import stomp
from stomp.utils import Frame

HOST = "localhost"
PORT = 61613

TOPIC_PRESS = "/topic/press"

MAX_MESSAGES = 20


class PressListener(stomp.ConnectionListener):

    def __init__(self, maxMessages: int, stopEvent: th.Event):
        self.maxMessages = maxMessages
        self.countMessages = 0
        self.stopEvent = stopEvent

    def on_message(self, frame: Frame):
        text = frame.body

        print(
            f"    [PRESS LISTENER] Ho ricevuto il messaggio {text}, lo aggiungo alla coda"
        )

        value = int(text)
        with open("press.csv", "a") as file:
            file.write(f"{self.countMessages},{value}\n")

        self.countMessages += 1
        if self.countMessages == self.maxMessages:
            print(
                f"    [PRESS LISTENER] Ho ricevuto {self.maxMessages} messaggi, termino"
            )
            self.stopEvent.set()


if __name__ == "__main__":
    with open("press.csv", "w") as file:
        file.write("Indice,Valore\n")

    conn = stomp.Connection([(HOST, PORT)], auto_content_length=False)

    conn.connect(wait=True)

    listenerStopped = th.Event()

    listener = PressListener(MAX_MESSAGES, listenerStopped)
    conn.set_listener("pressListener", listener)
    conn.subscribe(destination=TOPIC_PRESS, id=1, ack="auto")

    print(f"[PRESS ANALYZER] Attendo {MAX_MESSAGES} messaggi...")
    listenerStopped.wait()

    conn.disconnect()
