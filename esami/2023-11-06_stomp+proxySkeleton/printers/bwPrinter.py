import sys
import time
import stomp

from printerService.tipoStampa import TipoStampa

HOST_STOMP = "localhost"
PORT_STOMP = 61613

TIPI_VALIDI = [TipoStampa.BIANCO_NERO, TipoStampa.SCALA_GRIGI]

CODA_BW = "/queue/bw"

DELIMITER = "?"


class BWListener(stomp.ConnectionListener):
    def __init__(self, tipoStampa):
        super().__init__()
        self.tipoStampa = tipoStampa

    def on_message(self, frame: stomp.utils.Frame):
        message = frame.body

        splitted = message.split(DELIMITER)
        try:
            tipoStampa = TipoStampa(splitted[1])
            if tipoStampa != self.tipoStampa:
                print(f"[BW_LISTENER]   Skipped messaggio {message}")
                return
        except ValueError:
            print("[BW_LISTENER] Tipo di stampa non valido")
            return

        print(f"[BW_LISTENER] Ho ricevuto il messaggio {message}")

        with open("bw.txt", "a") as file:
            file.write(message + "\n")


if __name__ == "__main__":
    try:
        tipoStampa = TipoStampa(sys.argv[1])
        if tipoStampa not in TIPI_VALIDI:
            raise ValueError("Tipo non accettabile")

    except IndexError:
        print("Inserici il tipo da ascoltare per stampare")
        sys.exit(1)
    except ValueError:
        print(
            f"Tipo di stampa non riconosciuto, inserisci uno tra: {[str(tipo) for tipo in TIPI_VALIDI]}"
        )
        sys.exit(1)

    # si collega al provider stomp
    conn = stomp.Connection([(HOST_STOMP, PORT_STOMP)])

    conn.connect(wait=True)

    listener = BWListener(tipoStampa)
    conn.set_listener("bwListener", listener)
    conn.subscribe(destination=CODA_BW, id=1, ack="auto")

    print(f"[BW_LISTENER] In ascolto sulla destination {CODA_BW}")

    while True:
        time.sleep(1)

    conn.disconnect()
