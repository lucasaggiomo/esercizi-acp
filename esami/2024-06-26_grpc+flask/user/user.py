import grpc
import threading as th
import random
import sys

import laptopService_pb2 as laptopService
import laptopService_pb2_grpc as laptopService_grpc

NUM_THREADS = 10

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
            "Inserisci solo il numero di porto (default host = 'localhost') oppure l'indirizzo dell'host seguito dal numero di porto"
        )

    print(f"[USER] Provo ad aprire un canale verso il server {HOST}:{PORT}")

    # apra il canale di connessione verso il server
    with grpc.insecure_channel(f"{HOST}:{PORT}") as channel:
        # istanzia uno stub associato al canale
        stub = laptopService_grpc.LaptopServiceStub(channel)

        # effettua le richieste

        for i in range(NUM_THREADS):
            if i % 2 == 0:
                # vendita
                serial_number = random.randint(1, 100)
                print(
                    f"[USER] Invio una richiesta di vendita del laptop {serial_number}"
                )

                laptop = laptopService.Laptop(serial_number=serial_number)

                ack: laptopService.Ack = stub.sell(laptop)
                if ack.successful:
                    print(
                        f"      [USER] Vendita del laptop {serial_number} effettuata con successo!"
                    )
                else:
                    print(f"        [USER] La del laptop {serial_number} è fallita!")

            else:
                # acquisto
                print("[USER] Invio una richiesta di acquisto di un laptop")

                empty = laptopService.Empty()
                laptop: laptopService.Laptop = stub.buy(empty)

                serial_number = laptop.serial_number
                print(f"        [USER] Ho acquistato il laptop {serial_number}")
