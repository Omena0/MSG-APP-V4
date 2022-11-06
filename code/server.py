import lib
import SimpleSockets as ss
import config as c
from threading import Thread
import socket

main = socket.socket()
auth = socket.socket()

server_name = 'A test server'
server_id = 'TestServer'
server_password = '1234'

class user():
    def __init__(self,name,token,cs,ip,port):
        self.name = name
        self.token = token
        self.cs = cs
        self.ip = ip
        self.port
        self.ips = [ip]

# Send request to server for server discovery, this will be only way to join lmao

auth.send(f'GET-SERVERTOKEN {server_name.replace(":","")}:{server_id.replace(":","")}:{password.replace(":","")}'.encode())

# Response should be:
# X_Invalid_Id
# X_Invalid_Password
# X_Invalid_Name
# X_Valid_Credentials <name>:<id>:<token> 

while True:
    msg = auth.recv(1024).decode()
    if not msg.startswith('X_Valid_Credentials '):
        lib.log('ERROR',msg)
        while True: pass
    msg = msg.replace('X_Valid_Credentials ','').split(':')
    server_name = msg[0] # string without :
    server_id = msg[1] # int
    server_token = msg[2] # hash
    break



while True:
    cs, address = main.accept
