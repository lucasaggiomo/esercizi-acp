import requests

from prenotazioneService import IPrenotazioneService


class FlaskService(IPrenotazioneService):
    def __init__(self, address: str):
        self.address = address

    def create(
        self,
        client: str,
        hotel: str,
        operator: str,
        nights: int,
        people: int,
        cost: float,
    ) -> str:
        dictionary = {
            "client": client,
            "hotel": operator,
            "operator": operator,
            "nights": nights,
            "people": people,
            "cost": cost,
        }
        print("[FLASK SERVICE] Invio richiesta CREATE (post) di " + str(dictionary))
        response = requests.post(self.address, json=dictionary)

        try:
            response.raise_for_status()
            print(
                f"[FLASK SERVICE] Ricevuta la risposta: {response.text}, status code: {response.status_code}"
            )
        except requests.exceptions.HTTPError:
            print(
                f"[FLASK SERVICE] Errore nella risposta: {response.text}, status_code: {response.status_code}"
            )
        except Exception as e:
            print(f"[FLASK SERVICE] Errore generico: {e}")

        return response.text

    def update(self, discount: float, operator: str, nights: int) -> str:
        dictionary = {
            "discount": discount,
            "operator": operator,
            "nights": nights,
        }
        print("[FLASK SERVICE] Invio richiesta UPDATE (put) di " + str(dictionary))
        response = requests.put(self.address, json=dictionary)

        try:
            response.raise_for_status()
            print(
                f"[FLASK SERVICE] Ricevuta la risposta: {response.text}, status code: {response.status_code}"
            )
        except requests.exceptions.HTTPError:
            print(
                f"[FLASK SERVICE] Errore nella risposta: {response.text}, status_code: {response.status_code}"
            )
        except Exception as e:
            print(f"[FLASK SERVICE] Errore generico: {e}")

        return response.text
