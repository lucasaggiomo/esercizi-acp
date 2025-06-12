import stomp
from stomp.utils import Frame


class ClientListener(stomp.ConnectionListener):
    def __init__(self):
        super().__init__()
        
    def on_message(self, frame: Frame):
        # riceve il messaggio e lo stampa
        print(f"[CLIENT] Ho ricevuto {frame.body}")
