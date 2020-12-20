#!/usr/bin/env python
# coding: utf-8

# In[13]:


import socket  
import os
import threading
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import base64

 Create Socket (TCP) Connection
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.22'
port = 2223
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen()
HashTable = {}

AES_key = ""  # Later updated
n = 19*23
e = 13
d = 61
server_public_key = [e,n]
server_private_key = [d,n]

def rsa_encrypt(pub_key,n_text):
    e,n=pub_key
    x=''
    m=0
    for i in n_text:
        if(i.isupper()):
            m = ord(i)-65
            c=(m**e)%n
            x+=str(c)
            x+=','
        elif(i.islower()):               
            m= ord(i)-97
            c=(m**e)%n
            x+=str(c)
            x+=','
        elif(i.isspace()):
            spc=400
            x+=str(400)
            x+=','
    return x

def rsa_decrypt(priv_key,c_text):
    d,n=priv_key
    txt=c_text.split(',')[:-1]
    x=''
    m=0
    for i in txt:
        if(i=='400'):
            x+=' '
        else:
            m=(int(i)**d)%n
            m+=65
            c=chr(m)
            x+=c
    return x

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
            connection.send(str.encode('Connection Successful')) # Response Code for Connected Client 
            print('Connected : ',name)
            print('Connection denied : ',name)
            response = connection.recv(2048).decode()
            if response=='HELLO':
                connection.send(str.encode("{},{}".format(e, n)))
                response = connection.recv(2048).decode()
                AES_key = rsa_decrypt(server_private_key, response)
                print("AES key recieved")
                #print("AES Key:{}".format(AES_key))
                # Key exchange done *********************************************************************
                aes = AES.new(str.encode(AES_key), AES.MODE_ECB)
                
                filename='mytext.txt'
                
                with open(filename, 'rb') as f:
                    print("Sending encrypted file")
                    while True:
                        data = f.read(1024)
                        if len(data)==0:
                            break
                        encd = aes.encrypt(pad(data, AES.block_size))
                        encd = base64.b64encode(encd)
                        connection.send(encd)
                        #************************************************************************
                        
                        snt = base64.b64decode(encd)
                        snnt = unpad(aes.decrypt(snt), AES.block_size)
                        #print("Length of image after encryption {}".format(len(encd)))
                        #print("Sent thru connection:{}".format(encd))
                        #print("Base64 Decoded:{}".format(snt))
                        #print("AES Decoded:{}".format(aes.decrypt(snt)))
                        #print("unpadded:{}".format(snnt))
                        #print("Sent : {}".format(snnt))
        else:
            connection.send(str.encode('Login Failed')) # Response code for login failed

    connection.close()

'''
data = b"secret"
>>> key = get_random_bytes(16)
>>> cipher = AES.new(key, AES.MODE_CBC)
>>> ct_bytes = cipher.encrypt(pad(data, AES.block_size))
>>> iv = b64encode(cipher.iv).decode('utf-8')
>>> ct = b64encode(ct_bytes).decode('utf-8')
>>> result = json.dumps({'iv':iv, 'ciphertext':ct})
>>> print(result)
'''

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


