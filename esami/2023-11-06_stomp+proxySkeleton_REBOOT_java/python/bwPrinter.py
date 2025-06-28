# BW Printer. Implementa la ricezione sulla STOMP Queue bw e prevede come parametro di avvio (da
# terminale) una stringa tra bw o gs. Alla ricezione di ciascun messaggio, il listener STOMP di BW Printer
# estrae il contenuto del messaggio, verifica se esso contiene la stringa ricevuta in input e, in caso
# affermativo, scrive su file (bw.txt) e stampa a video il messaggio appena ricevuto

import stomp
import time
import sys

HOST = "localhost"
PORT = 61613

DESTINATION = "/queue/bw"


class Listener(stomp.ConnectionListener):
    def __init__(self, tipo: str):
        self.tipo = tipo

    def on_message(self, frame: stomp.utils.Frame):
        text = frame.body

        splitted = text.split("-")
        pathFile = splitted[0]
        tipo = splitted[1]

        if tipo == self.tipo:
            print(f"[LISTENER] Ho ricevuto il messaggio {text}")
            with open("bw.txt", "a") as file:
                file.write(text + "\n")
        else:
            print(f"[LISTENER] Ho SKIPPATO il messaggio {text}")


if __name__ == "__main__":
    try:
        tipo = sys.argv[1]
        if tipo != "gs" and tipo != "bw":
            raise ValueError("Tipo non valido")
    except (IndexError, ValueError):
        print("Inserisci il tipo da ascoltare ('gs' o 'bw')")
        sys.exit(1)

    conn = stomp.Connection([(HOST, PORT)], auto_content_length=False)

    listener = Listener(tipo)
    conn.set_listener("listener", listener)

    conn.connect(wait=True)
    conn.subscribe(DESTINATION, id=1, ack="auto")

    print(f"In ascolto sulla coda {DESTINATION}")

    while True:
        time.sleep(1)

    conn.disconnect()
