import abc

from printerService.tipoStampa import TipoStampa


class IPrinter(abc.ABC):
    @abc.abstractmethod
    def print(self, pathFile: str, tipo: TipoStampa):
        pass
