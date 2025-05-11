from threading import Thread
import time
import sys
from random import randint
from dispatcherProxy import DispatcherProxy


def threadFunc(address, port, num_richieste):
    proxy = DispatcherProxy(address, port)

    for i in range(num_richieste):
        time.sleep(randint(2, 4))

        command = randint(0, 3)
        print(f"[CLIENT] Invio il comando {command}")

        proxy.sendCommand(command)


NUM_THREADS = 5
NUM_RICHIESTE = 3

if __name__ == "__main__":

    try:
        ADDRESS = sys.argv[1]
        PORT = int(sys.argv[2])
    except:
        print("Porta non valida o non inserita")
        sys.exit(1)

    threads: list[Thread] = []

    for i in range(NUM_THREADS):
        t = Thread(target=threadFunc, args=(ADDRESS, PORT, NUM_RICHIESTE))
        t.start()

    for t in threads:
        t.join()

    print("[CLIENT] Ho terminato")
