import lib
import SimpleSockets as ss
import config as c


main = ss.connection(c.ip,c.port,'server',logging=True)
auth = ss.connection(c.authip,c.authport,'client',logging=True)

users = set()

class user():

    def __init__(self,name,token):
        self.name = name
        self.token = token
        users.add(self)
    def bind(self,name,value):
        exec(f'self.{name} = {value}')

def get_user(name):
    for user in users:
        if user.name == name:
            return user

def on_connect(cs,ip,port):
    lib.log('+',f'New connection from {ip}! [{port}]')

def on_msg(msg,cs,address):
    ip = address[0]
    port = address[1] # Syntax: AUTH REFRESH TOKEN <NAME>:<TOKEN>
    lib.log('CLIENT',msg)
    if msg.startswith('[AUTH] REFRESH TOKEN '):
        lib.log('*',f'{ip}:{port} REFRESH TOKEN')
        msg = msg.replace('[AUTH] REFRESH TOKEN ','')
        name = msg.split(':')[0]
        token = msg.split(':')[1]
        global var
        var = cs,name,token
        auth.send(f'[AUTH] VALIDATE TOKEN {ip}:{name}:{token}')
        



def on_disconnect(cs,ip,port):
    lib.log('-',f'User {get_user(cs).name} Disconnected!')
    exec(f'del({get_user(cs)})')
    
main.bind('connect',on_connect)
main.bind('msg',on_msg)
main.bind('disconnect',on_disconnect)




while True:
    msg = auth.socket.recv(auth.msgbits).decode()

    lib.log('AUTH',msg)

    if msg.startswith('X_'):
        global var
        cs = var[0]
        match msg:
            case 'X_Invalid_User': lib.log('!','X_Invalid_User'); cs.send(msg.encode())
            case 'X_Wrong_User': lib.log('!','X_Wrong_User'); cs.send(msg.encode())
            case 'X_Invalid_Token': lib.log('!','X_Invalid_Token'); cs.send(msg.encode())
            case 'X_Valid_Token':
                cs.send(msg.encode())
                name = var[1]
                token = var[2]
                a = user(name,token)
                a.bind('cs',f'"{cs}"')
            case _:
                lib.log('!',f'Invalid return: {msg}')
 

    
    



