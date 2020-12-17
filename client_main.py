
import socket,sys

hostname = sys.argv[1]
port = 65432
infolist = socket.getaddrinfo(hostname,port,socket.AF_INET,socket.SOCK_STREAM)
list1 = infolist[0]
socket_args = list1[0:3]
print(socket_args)
address = list1[4]
print(address)
# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(*socket_args)

# connect the client
# client.connect((target, port))

client.connect(address)

response = client.recv(2048)
# Input UserName
name = input(response.decode())

client.send(str.encode(name))
response = client.recv(2048)

# Input Password
password = input(response.decode())	
client.send(str.encode(password))

print(response)

with open('downloaded.txt', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = client.recv(1024)
        print('data=%s', repr(data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully got the file')
client.close()
print('connection closed')
