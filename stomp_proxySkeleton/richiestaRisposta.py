from __future__ import annotations

import enum
import random
import uuid


class TipoRichiesta(enum.StrEnum):
    DEPOSITA = "Deposita"
    PRELEVA = "Preleva"


DELIMITER = ":"


class Richiesta:
    def __init__(self, tipo: TipoRichiesta, id: int = -1):
        self.tipo = tipo
        self.id = id

    @staticmethod
    def generateRandomRichiesta() -> Richiesta:
        tipo = random.choice(list(TipoRichiesta))
        id = int(uuid.uuid1()) if tipo == TipoRichiesta.DEPOSITA else -1
        return Richiesta(tipo, id)

    # str -> Richiesta
    @staticmethod
    def parseRichiesta(msg: str) -> Richiesta:
        stuff = msg.split(DELIMITER)
        return Richiesta(TipoRichiesta(stuff[0]), stuff[1])

    # Richiesta -> str
    def __str__(self) -> str:
        return f"{self.tipo}{DELIMITER}{self.id}"


class Risposta:
    def __init__(self, tipo: TipoRichiesta, data: str):
        self.tipo = tipo
        self.data = data

    # str -> Risposta
    @staticmethod
    def parseRisposta(msg: str) -> Risposta:
        stuff = msg.split(DELIMITER)
        return Risposta(stuff[0], stuff[1])

    # Risposta -> str
    def __str__(self) -> str:
        return f"{self.tipo}{DELIMITER}{self.data}"
