import socket, sys

PORT = 65401
hostname = sys.argv[1]
infolist = socket.getaddrinfo(hostname,PORT,socket.AF_INET,socket.SOCK_STREAM)
list1  = infolist[0]
socket_args = list1[0:3]
print(socket_args)
address = list1[4]
print(address)
with socket.socket(*socket_args) as s:
	s.connect(address)
	s.sendall(b'hello')
	print('sent')
	data = s.recv(1024)
print('received',repr(data))
