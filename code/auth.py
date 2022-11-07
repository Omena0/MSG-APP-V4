import lib
import config as c
import socket
from threading import Thread
import time as t

main = socket.socket()
main.bind((c.authip,c.authport))
main.listen(5)

clients = set()
servers = []
ids = []

users = []
usernames = []

class user:      # USER CLASS 
    def __init__(self,name,psw):
        self.name = name
        if name in usernames:
            name = name + '_'
            while name not in usernames: name = name + str(lib.rand(1,9))
        usernames.append(name)
        self.psw = lib.hash(psw)
        self.generate_token()
        users.append(self)
        
    def bind(self,name,value):
        exec(f'self.{name} = {value}')
    def generate_token(self):
        self.token = f'{str(self.name)}<TOKEN>{lib.hash(str(lib.rand(-32767,32767))+str(self.name)+str(self.psw))}'
        

class server:    # SERVER CLASS
    def __init__(self,name,id,password):
        self.name = name
        self.id = id
        self.psw = password
        self.ips = []
        self.generate_token()
        ids.append(id)
        servers.append(self)
        self.ip = 'OFFLINE'
        self.port = 'OFFLINE'
            
    def generate_token(self):
        self.token = f'{str(self.id)}<TOKEN>{lib.hash(str(lib.rand(-32767,32767))+str(self.name)+str(self.psw))}'
    def bind(self,name,value):
        exec(f'self.{name} = "{value}"')

server('A test server','TestServer','1234')
user('Omena0','1234')

lib.log('*','Starting authentication service...')

def handle_client(cs,ip,port):
    clients.add(cs)
    while True:
        try: msg = cs.recv(1024).decode()
        except:
            lib.log('-',f'{ip} Disconnected.\n')
            clients.remove(cs)
            cs.close()
            return
        if msg != '': lib.log('REQUEST',msg)
        if msg.startswith('GET-SERVERTOKEN '):
            msg = msg.replace('GET-SERVERTOKEN ','').split(':')
            name = msg[0]
            id = msg[1]
            psw = msg[2]
            for i in enumerate(ids):
                index, i = i
                if i == id:
                    if servers[index].psw == psw:
                        token = servers[index].token
                        name = name.replace(":","")
                        servers[index].ips.append(ip)
                        servers[index].generate_token()
                        servers[index].bind('ip',ip)
                        servers[index].bind('port',port)
                        cs.send(f'X_Valid_Credentials {name}:{id}:{token}'.encode())
                        lib.log('*',f'Token sent to {ip} for {id}')
                    else:
                        cs.send(f'X_Invalid_Credentials'.encode())
                        continue
                else: continue
            cs.send('X_Invalid_Credentials'.encode())

        elif msg.startswith('GET-SERVERS'):
            msg = ''
            for server in servers:
                msg = f'{server.name},{server.ip},{server.port}:{msg}'
            cs.send(msg.encode())
            
        elif msg.startswith('GET-AUTHSTATUS '):
            msg = msg.replace('GET-AUTHSTATUS ','').split(':')
            name = msg[0]
            token = msg[1]
            if name not in usernames:
                cs.send('X_No_User'.encode())
                continue
            for name in enumerate(usernames):
                index = name[0]
                name = name[1]
                if name == usernames[index]:
                    if users[index].token == token:
                        cs.send('X_Valid_Token'.encode())
                        continue
            cs.send('X_Invalid_Token'.encode())
            continue

        elif msg.startswith('GET-TOKEN '):
            msg = msg.replace('GET-TOKEN ','').split(':')
            name = msg[0]
            psw = msg[1]
            if name not in usernames: cs.send('X_Invalid_User'.encode())
            for i in enumerate(usernames):
                index = i[0]
                username = i[1]
                if username == name:
                    if users[index].psw == psw:
                        users[index].generate_token()
                        cs.send(f'{users[index].token}'.encode())
                    else: cs.send('X_Invalid_Password'.encode())


        
def info():
    time = 0
    updatetime = 15 # MIN 0.5 OTHERWISE WILL BREAK!! DEFAULT 30, FOR DEV: 15
    print('')
    lib.log('INFO',f'Authentication server details:')
    lib.log('INFO',f'Servercount {len(servers)}')
    lib.log('INFO',f'Usercount: {len(users)}')
    lib.log('INFO',f'Uptime: {time}')
    print('')
    while True:
        t.sleep(0.1)
        time = round(time + 0.1,1)
        #print(time)
        if time % updatetime == 0.0:
            print('')
            lib.log('INFO',f'Authentication server details:')
            lib.log('INFO',f'Servercount {len(servers)}')
            lib.log('INFO',f'Usercount: {len(users)}')
            lib.log('INFO',f'Uptime: {time}')
            print('')

   
a = Thread(target=info)
a.daemon = True
a.start()

while True:
    cs, address = main.accept()
    lib.log('+',f'Connection from {address[0]}')
    a = Thread(target=handle_client,args=[cs,address[0],address[1]])
    a.daemon = True
    a.start()

















    
