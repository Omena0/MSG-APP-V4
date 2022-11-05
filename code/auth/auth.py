import lib
import SimpleSockets as ss
import config as c
import json as j
import socket

debug = False

main = ss.connection(c.ip,c.port,'server',logging=True)

users = []
usernames = []

class user:
    def __init__(self,username,psw,admin=False):
        self.admin = admin
        self.username = username
        self.pswhash = lib.hash(psw)
        self.generate_token()
        usernames.append(username)
        users.append(self)
    def generate_token(self):
        self.token = f'{str(self.username)}<TOKEN>{lib.hash(str(lib.rand(-32767,32767))+str(self.username)+str(self.pswhash))}'
    
user('Omena0','1234',admin=True)

def get_user(name):
    index = 0
    for name in usernames:
        if name == name: return users[index]
        index = index + 1


#print(get_user('Omena0').token)

def on_connect(cs,ip,port):
    lib.log('+',f'Connection established from {ip}:{port}')

def on_msg(msg,cs,address):
    ip = address[0]
    port = address[1]
    lib.log('REQUEST',msg)
    lib.log('REQUEST',f'[ IP: {ip} PORT: {port} ]')
    if msg.startswith('[AUTH] VALIDATE TOKEN '):
        msg = msg.replace('[AUTH] VALIDATE TOKEN ','').split(':')
        ip = msg[0]
        name = msg[1]
        token = msg[2]
        index = 0
        # Can return:
        # X_Invalid_user
        # X_Wrong_User
        # X_Invalid_Token
        # X_Valid_Token
        if not name in usernames: cs.send('X_Invalid_User'.encode()); return
        for username in usernames:
            if not username == name:
                index = index + 1
                continue
            if not token.split('<TOKEN>')[0] == name: cs.send('X_Wrong_User'.encode()); return
            if token == users[index].token:
                cs.send('X_Valid_Token'.encode())
                users[index].generate_token()
            else: cs.send('X_Invalid_Token'.encode()); return

    elif msg.startswith('[AUTH] GET TOKEN '):
        msg = msg.replace('[AUTH] GET TOKEN ','').split(':')
        name = msg[0]
        psw = msg[1]
        if not name in usernames:
            cs.send('X_Invalid_User'.encode())
            lib.log('!',f'Client from {ip} Recieved error [X_Invalid_User]')
            return
        if lib.hash(psw) == get_user(name).pswhash:
            cs.send(f'[AUTH] RETURN TOKEN: {get_user(name).token}'.encode())
            lib.log('!',f'Client from {ip} Requested token for user [{name}]')
        else:
            cs.send('X_Invalid_Password'.encode())
            lib.log('!',f'Client from {ip} Recieved error [X_Invalid_Password]')
            return
        
    else: cs.send('X_Invalid_Request'.encode()); lib.log('!',f'Client from {ip} Recieved error [X_Invalid_Request]')
    
def on_disconnect(cs,ip,port):
    lib.log('+',f'Client from {ip}:{port} disconnected')

main.bind('connect',on_connect)
main.bind('disconnect',on_disconnect)
main.bind('msg',on_msg)

lib.log('*',f'Authentication Service running on {c.ip}:{c.port}')

while debug == False: pass
