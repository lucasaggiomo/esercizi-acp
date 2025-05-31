import socket as s
import threading as th

BUFF_SIZE = 1024

def handleConnection(conn):
	message = conn.recv(BUFF_SIZE)
	message = message.decode("utf-8")
	print(f"Ho ricevuto {message}")
	message = "Ok bro".encode("utf-8")
	conn.send(message)

	conn.close()

if __name__ == '__main__':
	sock = s.socket(s.AF_INET, s.SOCK_STREAM)
	sock.bind(('localhost', 0))

	serverAddr = sock.getsockname()
	print(f"Server in ascolto su {serverAddr}")

	sock.listen()

	while True:
		conn, clientAddr = sock.accept()

		print(f"Connesso con {clientAddr}")

		handleConnection(conn)

	sock.close()
