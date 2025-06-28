import socket as s

from loggingService import ILogging
from tipoLog import TipoLog


# classe proxy che implementa la comunicazione lato client tramite socket per il servizio ILogging
class LoggingProxy(ILogging):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def log(self, messaggioLog: str, tipo: TipoLog):
        socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket.connect((self.host, self.port))

        msg = f"{messaggioLog}-{str(tipo)}"

        print(f"[PROXY] Invio {msg}")
        socket.send(msg.encode("utf-8"))

        socket.close()
