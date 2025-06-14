import stomp
from stomp.utils import Frame
import threading as th
import random
import sys
import time

import requests

from prenotazioneService import PrenotazioneRequest, decodeRequest, IPrenotazioneService
from stompService import StompService
from flaskService import FlaskService


HOST_STOMP = "localhost"
PORT_STOMP = 61613

RESPONSE_TOPIC = "/topic/response"
REQUEST_TOPIC = "/topic/request"

SERVER_ADDRESS = "http://127.0.0.1:5000"

NUM_CREATE = 4
NUM_UPDATE = 2

DELIMITER = "-"


class RequestListener(stomp.ConnectionListener):
    def __init__(
        self, conn: stomp.Connection, destination: str, service: IPrenotazioneService
    ):
        super().__init__()
        self.conn = conn
        self.destination = destination
        self.service = service

    def on_message(self, frame: Frame):
        print("[BOOKING MANAGER] Ho ricevuto " + frame.body)

        # delega ad un thread la gestione della richiesta
        t = th.Thread(
            target=handleRequest,
            args=(frame.body, self.conn, self.destination, self.service),
        )
        t.start()


def handleRequest(
    message: str,
    conn: stomp.Connection,
    destination: str,
    service: IPrenotazioneService,
):
    # decodifica la richiesta
    args = decodeRequest(message)

    if args == None:
        print("[BOOKING REQUEST] Errore di decodifica")
        # invia un messaggio di errore sul topic di risposta
        conn.send(destination, body="ERROR")
        return

        # inoltra la richiesta al servizio
        args = message.split(DELIMITER)

    try:
        request, args = args[0], args[1]
        response = ""

        match request:
            case PrenotazioneRequest.CREATE:
                response = service.create(
                    args["client"],
                    args["hotel"],
                    args["operator"],
                    int(args["nights"]),
                    int(args["people"]),
                    float(args["cost"]),
                )
            case PrenotazioneRequest.UPDATE:
                response = service.update(
                    float(args["discount"]), args["operator"], int(args["nights"])
                )

    except KeyError as e:
        print(f"[BOOKING MANAGER] Argomenti per la richiesta non validi: " + e)
        return None

    # invia la richiesta sul topic di risposta
    conn.send(destination, body=response)


if __name__ == "__main__":
    conn = stomp.Connection(host_and_ports=[(HOST_STOMP, PORT_STOMP)])

    # si connette al provider
    conn.connect(wait=True)

    conn.subscribe(destination=REQUEST_TOPIC, id=1, ack="auto")

    flaskRequestService = FlaskService(address=SERVER_ADDRESS)

    listener = RequestListener(conn, RESPONSE_TOPIC, flaskRequestService)
    conn.set_listener("listener", listener)

    print("[BOOKING MANAGER] Sono in attesa di richieste...")

    # resta in attesa
    while True:
        time.sleep(60)

    conn.disconnect()
