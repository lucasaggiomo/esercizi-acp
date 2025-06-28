import time
import stomp
import multiprocessing as mp

from server.printerImpl import PrinterImpl
from server.printerSkeleton import PrinterSkeleton
from printerService.tipoStampa import TipoStampa

DIM_CODA = 5

HOST_PRINTER = "localhost"
PORT_PRINTER = 0

HOST_STOMP = "localhost"
PORT_STOMP = 61613

CODA_COLOR = "/queue/color"
CODA_BW = "/queue/bw"

DELIMITER = "?"


def consumatoreFun(queue: mp.Queue, conn: stomp.Connection):
    while True:
        print(f"     [CONSUMATORE_FUN] Provo a prelevare dalla coda...")
        # preleva una richiesta dalla coda
        richiesta = queue.get()

        print(f"     [CONSUMATORE_FUN] Ho prelevato la richiesta {richiesta}")

        splitted = richiesta.split(DELIMITER)
        try:
            tipoStampa = TipoStampa(splitted[1])
        except ValueError:
            print("     [CONSUMATORE_FUN] Tipo richiesta non valido")
            continue

        destination = CODA_COLOR if tipoStampa == TipoStampa.COLOR else CODA_BW

        print(
            f"    [CONSUMATORE_FUN] Invio la richiesta {richiesta} sulla destination {destination}"
        )
        conn.send(destination, body=richiesta)


if __name__ == "__main__":
    queue = mp.Queue(maxsize=DIM_CODA)

    # istanzia il servizio reale
    printerService = PrinterImpl(queue)

    # istanzia lo skeleton per la comunicazione via rete
    skeleton = PrinterSkeleton(HOST_PRINTER, PORT_PRINTER, printerService)

    # si collega al provider stomp
    conn = stomp.Connection([(HOST_STOMP, PORT_STOMP)])
    conn.connect(wait=True)

    # avvia il consumatore
    consumatore = mp.Process(target=consumatoreFun, args=(queue, conn))
    consumatore.start()

    # avvia il servizio
    skeleton.runSkeleton()

    consumatore.join()

    conn.disconnect()
