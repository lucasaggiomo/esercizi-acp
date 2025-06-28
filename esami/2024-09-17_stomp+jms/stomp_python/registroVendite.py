import time
import stomp
import multiprocessing as mp
from typing import Optional

HOST = "localhost"
PORT = 61613

TOPIC_COMPRA = "/topic/compra"
TOPIC_VENDI = "/topic/vendi"

DIM_QUEUE = 10


class QueueWrapper:
    def __init__(
        self,
        queue: mp.Queue,
        lock: mp.Lock,
        prodCV: mp.Condition,
        consCV: mp.Condition,
        searcherCV: mp.Condition,
    ):
        self.queue = queue
        self.lock = lock
        self.prodCV = prodCV
        self.consCV = consCV
        self.searcherCV = searcherCV

    def inserisciCliente(self, cliente: dict[str, int]):
        with self.lock:

            while self.queue.full():
                self.prodCV.wait()

            # sono nel lock quindi la sincronizzazione della coda sarebbe ridondante e rallenterebbe il flusso di esecuzione
            self.queue.put_nowait(cliente)

            self.consCV.notify()
            self.searcherCV.notify_all()  # sveglia tutti i ricercatori

    def consumaCliente(self) -> dict[str, int]:
        with self.lock:

            while self.queue.empty():
                self.consCV.wait()

            # sono nel lock quindi la sincronizzazione della coda sarebbe ridondante e rallenterebbe il flusso di esecuzione
            cliente = self.queue.get_nowait()

            self.prodCV.notify()

        return cliente

    def _ricercaConsumazione(self, budgetMinimo: int) -> Optional[dict[str, int]]:
        # scorre tutta la coda fino a che non trova un cliente che vada bene
        # al termine (sia se ha trovato un cliente, sia se non l'ha trovato) ripristina la coda,
        # eccetto per l'eventuale cliente trovato
        clientiVisitati: list[dict[str, int]] = []

        cliente = None

        while not self.queue.empty():
            # preleva un cliente dalla coda e verifica se il suo budget è maggiore o uguale alla quotazione
            cliente: dict[str, int] = self.queue.get_nowait()

            # la traccia impone che gli elementi della coda siano dictionary del tipo {ID_cliente: budgetCliente}
            # il problema è che il consumatore (venditore) deve cercare per budget. Per accedere al budget senza
            # conoscere l'ID del cliente risulta necessario effettuare il codice che segue.
            # Una tupla sarebbe stata decisamente più indicata
            IDCliente, budget = next(iter(cliente.items()))

            # print(
            #     f"            [SEARCHING] Analizzo {IDCliente} con budget {budget}..."
            # )

            if budget >= budgetMinimo:
                # print(f"                [SEARCHING] OK!")
                break

            # print(f"                [SEARCHING] NOPE!")

            # segna di rimettere il cliente nella coda alla fine del ciclo
            clientiVisitati.append(cliente)

            # perde il riferimento del cliente (qualora il while termini, deve risultare che non è stato trovato)
            cliente = None

        # rimette in coda i clienti consumati, eccetto quello eventuale trovato {cliente}
        for clienteVisitato in clientiVisitati:
            self.queue.put_nowait(clienteVisitato)

        # None se non l'ha trovato (ha reincontrato un cliente già incontrato in precedenza)
        return cliente

    def consumaPrimoClienteConBudgetMinimo(self, budgetMinimo: int) -> dict[str, int]:
        count = 1

        with self.lock:

            print(f"     [SEARCHER - {budgetMinimo}] Tentativo {count}...")
            cliente = self._ricercaConsumazione(budgetMinimo)

            while cliente == None:
                self.searcherCV.wait()  # aspetta una prossima produzione
                count += 1
                print(f"     [SEARCHER - {budgetMinimo}] Tentativo {count}...")
                cliente = self._ricercaConsumazione(budgetMinimo)

            # se si trova qui, cliente è diverso da None
            # inoltre ha effettuato un consumo
            self.prodCV.notify()

        return cliente


def produttoreFun(queue: QueueWrapper, text: str):

    splitted = text.split("-")

    IDCliente = splitted[0]
    budget = int(splitted[1])

    cliente = {IDCliente: budget}

    print(f" [PRODUTTORE] Produco il cliente {cliente}")
    queue.inserisciCliente(cliente)


def consumatoreFun(queue: QueueWrapper, text: str):

    splitted = text.split("-")

    targa = splitted[0]
    quotazione = int(splitted[1])

    print(
        f" [CONSUMATORE] Ricerco il primo cliente con budget maggiore di {quotazione} per la targa {targa}"
    )

    cliente = queue.consumaPrimoClienteConBudgetMinimo(budgetMinimo=quotazione)
    IDCliente, budget = next(iter(cliente.items()))

    with open("vendite.csv", "a") as file:
        line = f"{targa},{IDCliente},{quotazione}"
        print(f"    [CONSUMATORE] Aggiungo la riga {line} al file 'vendite.csv'")
        file.write(line + "\n")


class CompraListener(stomp.ConnectionListener):
    def __init__(self, queue: QueueWrapper):
        super().__init__()
        self.queue = queue

    def on_message(self, frame: stomp.utils.Frame):
        text = frame.body

        print(f"[COMPRA_LISTENER] Ho letto il messaggio {text}")
        process = mp.Process(target=produttoreFun, args=(self.queue, text))
        process.start()


class VendiListener(stomp.ConnectionListener):
    def __init__(self, queue: QueueWrapper):
        super().__init__()
        self.queue = queue

    def on_message(self, frame: stomp.utils.Frame):
        text = frame.body

        print(f"[VENDI_LISTENER] Ho letto il messaggio {text}")
        process = mp.Process(target=consumatoreFun, args=(self.queue, text))
        process.start()


if __name__ == "__main__":

    with open("vendite.csv", "w") as file:
        file.write("targa,cliente,quotazione_auto\n")

    queue = mp.Queue(maxsize=DIM_QUEUE)
    lock = mp.Lock()
    prodCV = mp.Condition(lock)
    consCV = mp.Condition(lock)
    searcherCV = mp.Condition(lock)

    # i processi avranno riferimenti ad oggetti QueueWrapper diversi,
    # ma gli attributi si riferiranno alle stesse shared memory (oggetti condivisi multiprocessing)
    queueWrapper = QueueWrapper(queue, lock, prodCV, consCV, searcherCV)

    compraListener = CompraListener(queueWrapper)
    vendiListener = VendiListener(queueWrapper)

    conn1 = stomp.Connection([(HOST, PORT)], auto_content_length=False)
    conn1.connect(wait=True)
    conn1.set_listener("compraListener", compraListener)
    conn1.subscribe(destination=TOPIC_COMPRA, id=1, ack="auto")

    conn2 = stomp.Connection([(HOST, PORT)], auto_content_length=False)
    conn2.connect(wait=True)
    conn2.set_listener("vendiListener", vendiListener)
    conn2.subscribe(destination=TOPIC_VENDI, id=1, ack="auto")

    print("[REGISTRO_VENDITE] In ascolto su topic 'vendi' e 'compra'...")

    while True:
        time.sleep(1)

    conn1.disconnect()
    conn2.disconnect()
