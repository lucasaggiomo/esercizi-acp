import threading as th
import stomp
from stomp.utils import Frame
import matplotlib.pyplot as plt

HOST = "localhost"
PORT = 61613

TOPIC_TEMP = "/topic/temp"

MAX_MESSAGES = 20


class TempListener(stomp.ConnectionListener):

    def __init__(self, queue: list[int], maxMessages: int, stopEvent: th.Event):
        self.queue = queue
        self.maxMessages = maxMessages
        self.countMessages = 0
        self.stopEvent = stopEvent

    def on_message(self, frame: Frame):
        text = frame.body

        print(
            f"    [TEMP LISTENER] Ho ricevuto il messaggio {text}, lo aggiungo alla coda"
        )

        value = int(text)
        self.queue.append(value)

        self.countMessages += 1
        if self.countMessages == self.maxMessages:
            print(
                f"    [TEMP LISTENER] Ho ricevuto {self.maxMessages} messaggi, termino"
            )
            self.stopEvent.set()


if __name__ == "__main__":
    conn = stomp.Connection([(HOST, PORT)], auto_content_length=False)

    conn.connect(wait=True)

    listenerStopped = th.Event()
    queue: list[int] = []

    listener = TempListener(queue, MAX_MESSAGES, listenerStopped)
    conn.set_listener("tempListener", listener)
    conn.subscribe(destination=TOPIC_TEMP, id=1, ack="auto")

    print(f"[TEMP ANALYZER] Attendo {MAX_MESSAGES} messaggi...")
    listenerStopped.wait()

    conn.disconnect()

    print(f"[TEMP ANALYZER] Queste sono le temperature ottenute:")
    print(queue)

    plt.plot(queue)

    plt.title("lineplot temperature")
    plt.xlabel("Indice")
    plt.ylabel("Valore")

    plt.grid(visible=True)

    # Salva il grafico su file
    plt.savefig("tempLinePlot.png")
