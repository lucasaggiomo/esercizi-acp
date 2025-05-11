import socket as s
import sys

IP = 'localhost' 
try:
	PORT = int(sys.argv[1])
except:
	PORT = 8096

buffersize = 1024
sock = s.socket(s.AF_INET, s.SOCK_STREAM)

address = sock.getsockname()

print(f"Client {address}")
serverAddr = (IP, PORT)

if not sock.connect(serverAddr):
	print("Connessione fallita")
	sys.exit(0)

message = input("Inserisci un messaggio: ")
sock.send(message.encode("utf-8"))
message = sock.recv(buffersize).decode("utf-8")
print(f"Risposta ricevuta {message}")

sock.close()
