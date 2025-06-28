import random
import sys
import time

from loggingProxy import LoggingProxy
from tipoLog import TipoLog

NUM_LOG = 10
messaggioFromTipoDict: dict[TipoLog, list[str]] = {
    TipoLog.DEBUG: ["success", "checking"],
    TipoLog.INFO: ["success", "checking"],
    TipoLog.ERROR: ["fatal", "exception"],
}


def getRandomLog() -> tuple[str, TipoLog]:
    tipo = random.choice(list(TipoLog))
    messaggioLog = random.choice(messaggioFromTipoDict[tipo])
    return (messaggioLog, tipo)


if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except IndexError:
        print("Inserire la porta del server")
        sys.exit(1)

    HOST = sys.argv[2] if len(sys.argv) > 2 else "localhost"

    proxy = LoggingProxy(HOST, PORT)

    for _ in range(NUM_LOG):
        messaggioLog, tipo = getRandomLog()

        print(f"[CLIENT] Invio un log {messaggioLog} di tipo {tipo}")
        proxy.log(messaggioLog, tipo)

        time.sleep(1)
