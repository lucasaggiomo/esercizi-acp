import stomp

from prenotazioneService import (
    IPrenotazioneService,
    PrenotazioneRequest,
    generateRequest,
)


class StompService(IPrenotazioneService):
    def __init__(self, conn: stomp.Connection, destination: str):
        self.conn = conn
        self.destination = destination

    def sendMessage(self, message: str):
        print("[STOMP SERVICE] Invio il messaggio " + message)
        self.conn.send(destination=self.destination, body=message)

    def create(
        self,
        client: str,
        hotel: str,
        operator: str,
        nights: int,
        people: int,
        cost: float,
    ) -> str:
        messaggio = generateRequest(
            PrenotazioneRequest.CREATE,
            client,
            hotel,
            operator,
            nights,
            people,
            cost,
        )

        self.sendMessage(messaggio)

        return "sent"

    def update(self, discount: float, operator: str, nights: int) -> str:
        messaggio = generateRequest(
            PrenotazioneRequest.UPDATE, discount, operator, nights
        )

        self.sendMessage(messaggio)

        return "sent"
