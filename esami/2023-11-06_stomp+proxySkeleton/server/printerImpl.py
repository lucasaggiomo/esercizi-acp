import multiprocessing as mp

from printerService.printer import IPrinter
from printerService.printer import TipoStampa

DELIMITER = "?"


def produttoreFun(queue: mp.Queue, pathFile: str, tipoStampa: TipoStampa):
    richiesta = f"{pathFile}{DELIMITER}{str(tipoStampa)}"
    print(f"        [PRODUTTORE] Inserisco la richiesta {richiesta} nella coda")
    queue.put(richiesta)
    print(f"        [PRODUTTORE] Inserimento completato!")


class PrinterImpl(IPrinter):
    def __init__(self, queue: mp.Queue):
        self.queue = queue

    def print(self, pathFile: str, tipoStampa: TipoStampa):

        print(
            f"  [PRINTER_IMPL] Ricevuta richiesta di print del file {pathFile} con tipo {str(tipoStampa)}"
        )
        produttore = mp.Process(
            target=produttoreFun, args=(self.queue, pathFile, tipoStampa)
        )
        produttore.start()
