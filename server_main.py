#!/usr/bin/env python
# coding: utf-8

# In[5]:


#!/usr/bin/env python
# coding: utf-8

# In[13]:


import socket  
import os
import threading
import hashlib


# Create Socket (TCP) Connection
host = '10.0.0.69'
port = 65432
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT,1)

ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen()
HashTable = {}

# Function : For each client 
def threaded_client(connection):
    connection.send(str.encode('ENTER USERNAME : ')) # Request Username
    name = connection.recv(2048)
    connection.send(str.encode('ENTER PASSWORD : ')) # Request Password
    password = connection.recv(2048)
    password = password.decode()
    name = name.decode()
    password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
# REGISTERATION PHASE   
# If new user,  regiter in Hashtable Dictionary  
    if name not in HashTable:
        HashTable[name]=password
        connection.send(str.encode('Registeration Successful')) 
        print('Registered : ',name)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
        
    else:
# If already existing user, check if the entered password is correct
        if(HashTable[name] == password):
            #connection.send(str.encode('Connection Successful')) # Response Code for Connected Client 
            print('Connected : ',name)
            print('Connection denied : ',name)
            while True:
                
                filename='mytext.txt'
                f = open(filename,'rb')
                l = f.read(1024)
                while (l):
                    connection.send(l)
                    print('Sent ',repr(l))
                    l = f.read(1024)
                f.close()
                break
        else:
            connection.send(str.encode('Login Failed')) # Response code for login failed

    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Got connection from', address)
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)  
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
ServerSocket.close()


# In[ ]:




