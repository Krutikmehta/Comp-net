import socket
import time
HOST = '10.0.0.69'
PORT = 65401

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT,1)
	s.bind((HOST,PORT))
	s.listen()
	print('listening')
	conn, addr = s.accept()
	print('connected')
	with conn:
		data = conn.recv(1024)
		conn.sendall(data)
	s.close()
