import lib
import SimpleSockets as ss
import config as c
from threading import Thread
import socket

main = socket.socket()
auth = socket.socket()

auth.bind((c.ip,c.port))

server_name = 'A test server'
server_id = 'TestServer'
server_password = '1234'

clients = set()

class user():
    def __init__(self,name,token,cs,ip,port):
        self.name = name
        self.token = token
        self.cs = cs
        self.ip = ip
        self.port
        self.ips = [ip]

lib.log('*',f'Starting server...')
lib.log('*',f'Name: {server_name}')
lib.log('*',f'ID: {server_id}')

def handle_client(cs,ip,port):
    while True:
        try:
            msg = cs.recv(1024).decode()
            print(msg)
        except:
            lib.log('-',f'{ip} Disconnected.')
            clients.remove(cs)
            cs.close()
            break
        msg = msg.split('<SEP>')
        token = msg[1]
        name = msg[1].split('<TOKEN>')[0]
        msg = msg[0]
        auth.send(f'GET-AUTHSTATUS {name}:{token}'.encode())
        while True:
            a = auth.recv(1024).decode()
            if a == 'X_Invalid_Token':
                cs.close()
                clients.remove(cs)
                break
            else:
                a = frozenset(clients)
                for cs in a:
                    try:
                        cs.send(f'[MESSAGE]{name}<SEP>{msg.replace("<MSG>","")}<END>'.encode())
                    except: clients.remove(cs)
                break
        
        
# Send request to server for server discovery, this will be only way to join lmao
lib.log('*','Authenticating...')
try: auth.connect((c.authip,c.authport))
except ConnectionRefusedError:
    lib.log('!','Failed to authenticate! Authentication server offline!')
    while True: pass

auth.send(f'GET-SERVERTOKEN {server_name.replace(":","")}:{server_id.replace(":","")}:{server_password.replace(":","")}'.encode())

# Response should be:
# X_Invalid_Credentials
# X_Valid_Credentials <name>:<id>:<token> 

while True:
    msg = auth.recv(1024).decode()
    lib.log('AUTH',msg)
    if not msg.startswith('X_Valid_Credentials '):
        lib.log('ERROR',msg)
        while True: pass
    msg = msg.replace('X_Valid_Credentials ','').split(':')
    server_name = msg[0] # string without :
    server_id = msg[1] # int
    server_token = msg[2] # hash
    print()
    lib.log('!','Authentication complete! Starting main server...')
    lib.log('*',f'NAME: {server_name}')
    lib.log('*',f'ID: {server_id}')
    lib.log('*',f'TOKEN: {server_token}')
    print()
    break

auth.close()
auth = socket.socket()
auth.connect((c.authip,c.authport))

main.bind((c.ip,c.port))
main.listen(5)

lib.log('*','Address bound! Listening...')

while True:
    cs, address = main.accept()
    clients.add(cs)
    lib.log('+',f'Connection from {address[0]}')
    a = Thread(target=handle_client,args=[cs,address[0],address[1]])
    a.daemon = True
    a.start()
    sus = frozenset(clients)
    for cs in sus:
        try: cs.send('[+]{address[1]}'.encode())
        except: clients.remove(cs)
