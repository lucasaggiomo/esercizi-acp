import abc

from tipoLog import TipoLog


class ILogging(abc.ABC):
    @abc.abstractmethod
    def log(self, messaggioLog: str, tipo: TipoLog):
        pass
