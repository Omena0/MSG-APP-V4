import SimpleSockets as ss
import lib

ip = '127.0.0.1'
port = 5000

authip = '127.0.0.1'
authport = 5001

#main = ss.connection(ip,port,'client',logging=True)
auth = ss.connection(authip,authport,'client',logging=True)

def on_msg(msg, cs, address):
    lib.log('MSG',msg)

# Auth server returns this:
# [AUTH] RETURN TOKEN: Omena0<TOKEN>31dbc24007771df22a8bd31bbc269bcc2dc7bfb5
# We handle it here:
def on_auth_msg(msg, cs, address):
    print('hellooooo')
    if msg.startswith('X_'): lib.log('AUTH',f'Returned error: {msg}')
    else: lib.log('AUTH',msg)
    
    if msg.startswith('[AUTH] RETURN TOKEN: '):
        msg = msg.replace('[AUTH] RETURN TOKEN: ','')
        token = msg
        name = msg.split('<TOKEN>')[0]
        lib.log('!',f'Logged in as {name}')
        

#main.bind('msg',on_msg)
auth.bind('msg',on_auth_msg)

username = 'Omena0'
password = '1234'

auth.send(f'[AUTH] GET TOKEN {username}:{password}')

while True:
    print(auth.socket.recv(auth.msgbits).decode())
