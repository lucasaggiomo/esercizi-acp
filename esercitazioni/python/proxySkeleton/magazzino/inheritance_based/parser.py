from operation import Operation
from articolo import Articolo

SEPARATOR = "#"


def generateCommand(operazione: Operation, articolo: Articolo, id: int = -1) -> str:
    return SEPARATOR.join((operazione, articolo, str(id)))


def parseCommand(command: str) -> tuple[Operation, Articolo, int]:
    op_str, art_str, id_str = command.split(SEPARATOR)
    return Operation(op_str), Articolo(art_str), int(id_str)
