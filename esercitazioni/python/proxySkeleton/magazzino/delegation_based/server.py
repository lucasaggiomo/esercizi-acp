import sys

from magazzinoImpl import MagazzinoImpl
from magazzinoSkeleton import MagazzinoSkeleton

QUEUE_SIZE = 5

if __name__ == "__main__":
    try:
        ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        PORT = sys.argv[2] if len(sys.argv) > 2 else 0
    except:
        print(
            "[SERVER] Indirizzo e numero di porta del server non inseriti correttamente"
        )
        sys.exit(1)

    magazzino = MagazzinoImpl(QUEUE_SIZE)
    skel = MagazzinoSkeleton(ADDRESS, PORT, magazzino)
    skel.runSkeleton()
