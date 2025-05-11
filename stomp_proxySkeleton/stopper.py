import stomp
from utils import getFromArgvOrDefault

if __name__ == "__main__":
    HOST = getFromArgvOrDefault(1, "127.0.0.1")
    PORT = getFromArgvOrDefault(2, 61613)
    print(f"Address: {HOST}, Port: {PORT}")

    conn = stomp.Connection([(HOST, PORT)])
    conn.connect(wait=True)

    conn.send("/topic/stop", "STOP")

    conn.disconnect()
