import prodConsQueue as pc
from magazzinoSkeleton import MagazzinoSkeleton
from articolo import Articolo


class MagazzinoImpl(MagazzinoSkeleton):

    def __init__(self, dim: int, address: str, port: int):
        super().__init__(address, port)

        self.queueMap: dict[Articolo, tuple[pc.Queue, str]] = {}
        for articolo in Articolo:
            self.queueMap[articolo] = (pc.Queue(dim), articolo + ".txt")

    def preleva(self, articolo: Articolo) -> int:
        queue, filePath = self.queueMap[articolo]
        id = queue.consume()

        with open(filePath, "a") as file:
            file.write(f"{id}\n")

        return id

    def deposita(self, articolo: Articolo, id: int) -> None:
        queue, filePath = self.queueMap[articolo]
        queue.produce(id)

        with open(filePath, "a") as file:
            file.write(f"{id}\n")
