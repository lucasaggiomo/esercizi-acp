import abc
import enum


class IPrenotazioneService(abc.ABC):
    @abc.abstractmethod
    def create(
        self,
        client: str,
        hotel: str,
        operator: str,
        nights: int,
        people: int,
        cost: float,
    ) -> str:
        pass

    @abc.abstractmethod
    def update(self, discount: float, operator: str, nights: int) -> str:
        pass


class PrenotazioneRequest(enum.StrEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"


DELIMITER = "#"


def generateRequest(request: PrenotazioneRequest, *args) -> str:
    message = str(request)
    if len(args) > 0:
        message += DELIMITER
    for i in range(len(args)):
        message += str(args[i])
        if i < len(args) - 1:
            message += DELIMITER
    return message


def decodeRequest(message: str) -> dict[str, str]:
    args = message.split(DELIMITER)

    try:
        request = PrenotazioneRequest(args[0])
        output: dict[str, str] = {}

        match request:
            case PrenotazioneRequest.CREATE:
                output["client"] = args[1]
                output["hotel"] = args[2]
                output["operator"] = args[3]
                output["nights"] = args[4]
                output["people"] = args[5]
                output["cost"] = args[6]
            case PrenotazioneRequest.UPDATE:
                output["discount"] = args[1]
                output["operator"] = args[2]
                output["nights"] = args[3]

        return request, output

    except ValueError:
        print(f"[DECODE REQUEST] Richiesta '{request}' non riconosciuta")
        return None
    except IndexError:
        print(f"[DECODE REQUEST] Argomenti per la richiesta non sufficienti")
        return None
