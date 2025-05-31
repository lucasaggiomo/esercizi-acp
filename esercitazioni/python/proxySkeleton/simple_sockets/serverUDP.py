import socket as s

IP = 'localhost'
PORT = 0

buffersize = 1024

sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
sock.bind((IP, PORT))

address = sock.getsockname()
print(f"In ascolto {address}")

while True:
	message, clientAddr = sock.recvfrom(buffersize)
	message = message.decode("utf-8")

	print(f"{clientAddr} mi ha mandato il seguente messaggio:") 
	print(message)

	if message == "EXIT":
		break

sock.close()

