import socket as s
import sys

IP = 'localhost' 
try:
	PORT = int(sys.argv[1])
except:
	PORT = 8096

buffersize = 1024
sock = s.socket(s.AF_INET, s.SOCK_DGRAM)

address = sock.getsockname()

print(f"Client {address}")
serverAddr = (IP, PORT)

while True:
	message = input("Inserisci un messaggio: ")
	sock.sendto(message.encode("utf-8"), serverAddr)
	if message == "EXIT":
		break

sock.close()
