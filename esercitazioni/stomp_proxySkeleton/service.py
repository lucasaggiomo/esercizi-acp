import abc


class Service(abc.ABC):
    @abc.abstractmethod
    def preleva(self) -> int:
        pass

    @abc.abstractmethod
    def deposita(self, id: int) -> str:
        pass
