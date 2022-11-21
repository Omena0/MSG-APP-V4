import lib
import config as c
from threading import Thread
import socket
import os

main = socket.socket()
auth = socket.socket()

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
lib.log('*',f'Name: {c.server_name}')
lib.log('*',f'ID: {c.server_id}')
lib.log('*',f'Tunnel IP: {c.server_ip}')
lib.log('*',f'Tunnel PORT: {c.server_port}')

lib.log('PLUGIN LOADER','Searching for plugins')
import plugins as p
if not p.plugins == []:
    for i in p.plugins:
        i.on_init()


def handle_client(cs,ip,port):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except:
            try:
                lib.log('-',f'{ip} Disconnected.')
                for i in p.plugins:
                    i.on_leave(ip,port)
                clients.remove(cs)
                cs.close()
                break
            except: break
        msg = msg.split('<SEP>')
        token = msg[1]
        name = msg[1].split('<TOKEN>')[0]
        msg = msg[0]
        auth.send(f'GET-AUTHSTATUS {name}:{token}'.encode())
        while True:
            a = auth.recv(1024).decode()
            for i in p.plugins:
                i.on_login(name,ip,port,a)
            if a == 'X_Invalid_Token' or a == 'X_Invalid_Password' or a == 'X_No_User':
                cs.close()
                clients.remove(cs)
                break
            else:
                a = frozenset(clients)
                for cs in a:
                    try:
                        cs.send(f'[MESSAGE]{name}<SEP>{msg.replace("<MSG>","")}<END>'.encode())
                        for i in p.plugins:
                            i.on_msg(name,msg,ip)
                        lib.log('MESSAGE',f'<{name}>: {msg.replace("<MSG>","")}')
                    except: clients.remove(cs)
                break
        
        
# Send request to server for server discovery, this will be only way to join lmao
lib.log('*','Authenticating...')
try: auth.connect((c.authip,c.authport))
except ConnectionRefusedError as e:
    lib.log('!','Failed to authenticate! Authentication server offline!')
    if input('') == 'debug': print(f'\n{e}\n')
    while True: pass

auth.send(f'GET-SERVERTOKEN {c.server_name.replace(":","")}:{c.server_id.replace(":","")}:{c.server_password.replace(":","")}:{c.server_ip.replace(":","")}:{str(c.server_port).replace(":","")}'.encode())

# Response should be:
# X_Invalid_Credentials
# X_Valid_Credentials <name>:<id>:<token> 

while True:
    msg = auth.recv(1024).decode()
    lib.log('AUTH',msg)
    if not msg.startswith('X_Valid_Credentials '):
        lib.log('ERROR',msg)
        if input('') == 'debug': print(f'\n{e}\n')
        while True: pass
    msg = msg.replace('X_Valid_Credentials ','').split(':')
    c.server_name = msg[0] # string without :
    c.server_id = msg[1] # int
    c.server_token = msg[2] # hash
    print()
    lib.log('!','Authentication complete! Starting main server...')
    lib.log('*',f'NAME: {c.server_name}')
    lib.log('*',f'ID: {c.server_id}')
    lib.log('*',f'TOKEN: {c.server_token}')
    print()
    break

auth.close()
auth = socket.socket()
auth.connect((c.authip,c.authport))

main.bind((c.ip,c.port))
main.listen(0)

lib.log('*',f'Address bound! Listening... ({c.server_ip}:{c.server_port} => {c.ip}:{c.port})')

while True:
    cs, address = main.accept()
    clients.add(cs)
    lib.log('+',f'Connection from {address[0]}')
    for i in p.plugins:
        i.on_join(address[0],address[1])
    a = Thread(target=handle_client,args=[cs,address[0],address[1]])
    a.daemon = True
    a.start()
    sus = frozenset(clients)
    for cs in sus:
        try: cs.send('[+]{address[1]}'.encode())
        except: clients.remove(cs)
