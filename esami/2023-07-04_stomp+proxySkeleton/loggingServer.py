import multiprocessing as mp

import stomp
from loggingSkeleton import LoggingSkeleton
from tipoLog import TipoLog

QUEUE_CAPACITY = 5

SKEL_HOST = "localhost"
SKEL_PORT = 0

STOMP_HOST = "localhost"
STOMP_PORT = 61613


# implementazione dello skeleton (Proxy-Skeleton con ereditarietà),
# che implementa il servizio di logging attraverso il paradigma produttore-consumatore
class LoggingImpl(LoggingSkeleton):
    def __init__(self, queue: mp.Queue, host: str, port: int):
        super().__init__(host, port)
        self.queue = queue

    def log(self, messaggioLog: str, tipo: TipoLog):
        msg = f"{messaggioLog}-{str(tipo)}"
        self.queue.put(msg)


def consumatoreFunction(queue: mp.Queue):
    while True:
        # legge il prossimo messaggio di log (bloccante)
        msg: str = queue.get()

        # preleva il tipo di log e determina la coda di destinazione
        splitted = msg.split("-")
        tipo = TipoLog(int(splitted[1]))
        destination = "/queue/error" if tipo == TipoLog.ERROR else "/queue/info"

        print(
            f"[SERVER_CONSUMATORE] Ho consumato il messaggio {msg}, lo invio sulla coda {destination}"
        )
        # invia il messaggio sulla Queue STOMP associata
        conn = stomp.Connection([(STOMP_HOST, STOMP_PORT)])
        conn.connect(wait=True)

        conn.send(destination=destination, body=msg)

        conn.disconnect()


if __name__ == "__main__":
    queue = mp.Queue(QUEUE_CAPACITY)

    consumatore = mp.Process(target=consumatoreFunction, args=(queue,))
    consumatore.start()

    logging = LoggingImpl(queue, SKEL_HOST, SKEL_PORT)
    logging.runSkeleton()

    consumatore.join()
