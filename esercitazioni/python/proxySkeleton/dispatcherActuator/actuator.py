import time
import sys
from dispatcherProxy import DispatcherProxy
from datetime import datetime

LOG_FILE = "cmdlog.txt"

if __name__ == "__main__":
    try:
        ADDRESS = sys.argv[1]
        PORT = int(sys.argv[2])
    except:
        print("Porta non valida o non inserita")
        sys.exit(1)

    proxy = DispatcherProxy(ADDRESS, PORT)

    commandDict = {0: "leggi", 1: "scrivi", 2: "configura", 3: "reset"}

    while True:
        time.sleep(1)

        command = proxy.getCommand()

        print(f"[ACTUATOR] Ricevuto {command} - {commandDict[command]}")

        with open(LOG_FILE, "a") as logger:
            logger.write(str(datetime.now()) + " " + commandDict[command] + "\n")
