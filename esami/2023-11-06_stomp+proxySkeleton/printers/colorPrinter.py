import sys
import time
import stomp

HOST_STOMP = "localhost"
PORT_STOMP = 0

ESTENSIONI_VALIDE = ["doc", "txt"]

CODA_COLOR = "/queue/color"
PORT_STOMP = 61613

DELIMITER = "?"


class ColorListener(stomp.ConnectionListener):
    def __init__(self, estensioneFile):
        super().__init__()
        self.estensioneFile = estensioneFile

    def on_message(self, frame: stomp.utils.Frame):
        message = frame.body

        splitted = message.split(DELIMITER)
        estensioneFile = splitted[0].split(".")[1]
        if estensioneFile != self.estensioneFile:
            print(f"    [COLOR_LISTENER] Skipped messaggio {message}")
            return

        print(f"[COLOR_LISTENER] Ho ricevuto il messaggio {message}")

        with open("color.txt", "a") as file:
            file.write(message + "\n")


if __name__ == "__main__":
    try:
        estensioneFile = sys.argv[1]
        if estensioneFile not in ESTENSIONI_VALIDE:
            raise ValueError("Tipo non accettabile")

    except IndexError:
        print("Inserici l'estensione di file da osservare")
        # sys.exit(1)
        estensioneFile = "doc"
    except ValueError:
        print(
            f"Estensione di file non supportata, inserisci una tra: {ESTENSIONI_VALIDE}"
        )
        sys.exit(1)

    # si collega al provider stomp
    conn = stomp.Connection([(HOST_STOMP, PORT_STOMP)])

    conn.connect(wait=True)

    listener = ColorListener(estensioneFile)
    conn.set_listener("colorListener", listener)
    conn.subscribe(destination=CODA_COLOR, id=1, ack="auto")

    print(f"[COLOR_LISTENER] In ascolto sulla destination {CODA_COLOR}")

    while True:
        time.sleep(1)

    conn.disconnect()
