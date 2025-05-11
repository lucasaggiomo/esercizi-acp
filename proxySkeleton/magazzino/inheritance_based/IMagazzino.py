from abc import ABC, abstractmethod

from articolo import Articolo


class IMagazzino(ABC):

    @abstractmethod
    def deposita(self, articolo: Articolo, id: int) -> None:
        pass

    @abstractmethod
    def preleva(self, articolo: Articolo) -> int:
        pass
