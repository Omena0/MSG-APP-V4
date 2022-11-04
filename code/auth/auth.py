import lib
import SimpleSockets as ss
import config as c
import json as j

main = ss.connection(c.ip,c.port,'server',logging=True)

users = []
usernames = []

class user:
    def __init__(self,username,psw,admin=False):
        self.admin = admin
        self.username = username
        self.pswhash = lib.hash(psw)
        self.token = lib.hash(str(lib.rand(-32767,32767))+str(username)+str(lib.hash(psw))),str(username)
        usernames.append(username)
        users.append(self)

user('Omena0','1234',admin=True)

def on_connect(cs,ip,port):
    lib.log('+',f'Connection established from {ip}:{port}')

def on_msg(msg,cs,address):
    if msg.startswith('[AUTH] '):
        msg = msg.replace('[AUTH] ','').split(':')
        ip = msg[0]
        name = msg[1]
        token = msg[2]
        lib.log('*',f'[AUTH] {ip} Sent a request to authenticate as {name}! Token = {token}')
        index = 0
        if name in usernames:
            for username in usernames:
                if username == name:
                    if token == users[index].token: cs.send('X_Valid_Token'.encode())
                    else: cs.send('X_Invalid_Token
                                  '.encode())
                else: index = index + 1
        else: cs.send('X_Invalid_User'.encode())
        
def on_disconnect(cs,ip,port):
    lib.log('+',f'Client from {ip}:{port} disconnected')

main.bind('connect',on_connect)
main.bind('disconnect',on_disconnect)
main.bind('msg',on_msg)

lib.log('*',f'Server running on {c.ip}:{c.port}')

