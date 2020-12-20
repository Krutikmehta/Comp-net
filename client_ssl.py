#!/usr/bin/env python
# coding: utf-8

# In[14]:


import socket
import random
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import base64

AES_key = 'AITFKECYRHQPFYBG'
#print(AES_key)
server_public_key = [0,0]  # e, n


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



# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))

client.connect(('127.0.0.22', 2223))

response = client.recv(2048)
# Input UserName
name = input(response.decode())

client.send(str.encode(name))
response = client.recv(2048)

# Input Password
password = input(response.decode())	
client.send(str.encode(password))
''' Response : Status of Connection :
	1 : Registeration successful 
	2 : Connection Successful
	3 : Login Failed
'''
# Receive response 
response = client.recv(2048)
response = response.decode()
print(response)


if response== 'Connection Successful':
    client.send(str.encode("HELLO"))
    response = client.recv(2048).decode().split(',')
    server_public_key[0] = int(response[0]) #e
    server_public_key[1] = int(response[1]) #n

    client.send(str.encode(rsa_encrypt(server_public_key, AES_key)))
    aes = AES.new(str.encode(AES_key), AES.MODE_ECB)
    
    with open('received_file.txt', 'wb') as f:
        print("file opened")
        print('receiving data...')
        while True:
            rec = client.recv(2048)
            data = base64.b64decode(rec)
            data_len = len(data)
            if data_len == 0:
                break
            decd = unpad(aes.decrypt(data), AES.block_size)
            #decd = unpad(aes.decrypt(data), AES.block_size)
            #print("recieved:{}".format(rec))
            #print("base64 decrypted:{}".format(data))
            #print('aes decrypted:{}'.format(decd))
            f.write(decd)
        f.close()

'''
b64 = json.loads(json_input)
>>>     iv = b64decode(b64['iv'])
>>>     ct = b64decode(b64['ciphertext'])
>>>     cipher = AES.new(key, AES.MODE_CBC, iv)
>>>     pt = unpad(cipher.decrypt(ct), AES.block_size)
>>>     print("The message was: ", pt)
'''


print('Successfully got the file')
client.close()
print('connection closed')




