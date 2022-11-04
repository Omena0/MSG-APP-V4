import lib
import SimpleSockets as ss
import config as c


main = ss.connection(c.ip,c.port,'server',logging=True)
auth = ss.connection(c.authip,c.authport,'client',logging=True)

users = set()

class user():

    def __init__(self,name,token,ip,port,cs):
        self.name = name
        self.token = token
        self.ip = ip
        self.port = port
        self.cs = cs
        users.add(self)
    def bind(self,name,value):
        exec(f'self.{name} = {value}')

def get_user(name):
    for user in users:
        if user.name == name:
            return user

def authorise(msg,cs,address):
    lib.log('AUTH',msg)
    if msg == '[FAIL]':
        cs.close()
        main.clients.remove(cs)
        
    msg = msg.replace('[AUTH]','').split(':')
    name = msg[0]
    token = msg[1]
    ip = address[0]
    port = address[1]
    user(name,token,ip,port,cs)

def on_connect(cs,ip,port):
    lib.log('+',f'New connection from {ip}! [{port}]')

def on_msg(msg,cs,address):
    ip = address[0]
    port = address[1]
    lib.log('CLIENT',msg)
    if msg.startswith('[AUTH] REFRESH TOKEN '):
        lib.log('AUTH',f'{ip}:{port} REFRESH TOKEN')
        msg = msg.replace('[AUTH] REFRESH TOKEN ','')
        name = msg.split(':')[0]
        token = msg.split(':')[1]
        auth.send(f'[AUTH] {ip}:{name}:{token}')

def on_disconnect(cs,ip,port):
    lib.log('-',f'User {get_user(cs).name} Disconnected!')
    exec(f'del({get_user(cs)})')
    
main.bind('connect',on_connect)
main.bind('msg',on_msg)
main.bind('disconnect',on_disconnect)

auth.bind('msg',authorise)









