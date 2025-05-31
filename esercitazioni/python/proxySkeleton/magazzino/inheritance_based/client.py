import threading as th
import random
import time
import sys

from magazzinoProxy import MagazzinoProxy
from operation import Operation
from articolo import Articolo


def threadFunction(address: str, port: int, service: Operation):
    proxy = MagazzinoProxy(address, port, TIMEOUT)

    match service:
        case Operation.DEPOSITA:
            for i in range(NUM_REQUESTS):
                articolo = random.choice(list(Articolo))
                id = random.randint(1, 100)

                print(
                    f"[CLIENT - {th.current_thread().name}] Deposito l'articolo {(articolo.value, id)}"
                )

                res = proxy.deposita(articolo, id)
                if res == -1:
                    print(f"[CLIENT - {th.current_thread().name}] TIMEOUT")
                    return

                time.sleep(random.randint(2, 4))

        case Operation.PRELEVA:
            for i in range(NUM_REQUESTS):
                articolo = random.choice(list(Articolo))

                print(
                    f"[CLIENT - {th.current_thread().name}] Prelevo l'articolo {articolo}..."
                )

                id = proxy.preleva(articolo)
                if id == -1:
                    print(f"[CLIENT - {th.current_thread().name}] TIMEOUT")
                    return

                print(
                    f"[CLIENT - {th.current_thread().name}] Ho prelevato l'articolo {(articolo.value, id)}"
                )

                time.sleep(random.randint(2, 4))


NUM_THREADS = 5
NUM_REQUESTS = 3
TIMEOUT = 30

if __name__ == "__main__":
    try:
        ADDRESS = sys.argv[1]
        PORT = int(sys.argv[2])
        SERVICE = Operation[sys.argv[3].upper()]
    except IndexError:
        print(
            "[CLIENT] Indirizzo e numero di porta del server non inseriti correttamente"
        )
        sys.exit(1)

    threads: list[th.Thread] = []
    for _ in range(NUM_THREADS):
        t = th.Thread(target=threadFunction, args=(ADDRESS, PORT, SERVICE))
        t.start()

    for t in threads:
        t.join()

    print(f"[CLIENT - {th.current_thread().name}] Ho finito")
