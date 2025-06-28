import sys
import time
import random

from client.printerProxy import PrinterProxy
from printerService.tipoStampa import TipoStampa

NUM_STAMPE = 10

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            HOST = "localhost"
            PORT = int(sys.argv[1])
        else:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
    except IndexError:
        print(
            "Inserisci l'host e il numero di porta del server, oppure solo il numero di porta [default host = 'localhost']"
        )
        sys.exit(1)

    proxy = PrinterProxy(HOST, PORT)

    estensioni = ["txt", "doc"]

    for _ in range(NUM_STAMPE):
        num = random.randint(0, 100)
        ext = random.choice(estensioni)

        pathFile = f"/user/file_{num}.{ext}"
        tipoStampa = random.choice(list(TipoStampa))

        print(
            f"[USER] Effettuo una richiesta di stampa del file {pathFile} con tipo {str(tipoStampa)}"
        )
        proxy.print(pathFile, tipoStampa)

        time.sleep(1)
