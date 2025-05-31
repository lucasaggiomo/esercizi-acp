import prodConsQueue as pc
from IMagazzino import IMagazzino
from articolo import Articolo


class MagazzinoImpl(IMagazzino):

    def __init__(self, dim: int):
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
