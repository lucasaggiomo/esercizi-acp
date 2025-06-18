import requests

from tipoRichiesta import TipoRichiesta


class HistoryService:
    def __init__(self, historyServerURL: str):
        self.historyServerURL = historyServerURL

    def update_history(self, tipo: TipoRichiesta, serial_number: int):

        json = {"operation": str(tipo), "serial_number": serial_number}
        print(f"        [SERVICER] Notifico l'history server con {json}")

        try:
            response = requests.post(
                f"{self.historyServerURL}/update_history", json=json
            )
            response.raise_for_status()
            rispostaJson = response.json()
            print(
                f"          [SERVICER] Ho ricevuto la risposta {rispostaJson} con status code {response.status_code}"
            )
        except requests.HTTPError as e:
            print(f"        [SERVICER] Errore HTTP: {str(e)}")
        except requests.exceptions.JSONDecodeError:
            print(
                f"          [SERVICER] La risposta dell'history server non era in json '{response.text}' con status code {response.status_code}"
            )
