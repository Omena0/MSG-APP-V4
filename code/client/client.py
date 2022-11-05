import SimpleSockets as ss
import lib
from threading import Thread

ip = '127.0.0.1'
port = 5000

authip = '127.0.0.1'
authport = 5001

main = ss.connection(ip,port,'client',logging=True)
auth = ss.connection(authip,authport,'client',logging=True)



username = 'Omena0'
password = '1234'

auth.send(f'[AUTH] GET TOKEN {username}:{password}')

# Auth server returns this:
# [AUTH] RETURN TOKEN: Omena0<TOKEN>31dbc24007771df22a8bd31bbc269bcc2dc7bfb5
# We handle it here because the ss way didint work i guess

while True:
    msg = auth.socket.recv(1024).decode()
    if msg.startswith('X_'): lib.log('AUTH',f'Returned error: {msg}')
    else: lib.log('AUTH',msg)
    
    if msg.startswith('[AUTH] RETURN TOKEN: '):
        msg = msg.replace('[AUTH] RETURN TOKEN: ','')
        token = msg
        name = msg.split('<TOKEN>')[0]
        lib.log('!',f'Logged in as {name}')
        lib.log('!','Authenticating into msg server...')
        main.send(f'[AUTH] REFRESH TOKEN {name}:{token}')
    msg = main.socket.recv(1024).decode()
    lib.log('MSG',msg)
    if msg == 'X_Valid_Token': lib.log('*','Done!!!')
    break

def a():
    while True:
        main.send(input())

a = Thread(target=a)
a.daemon=True
a.start()

while True:
    msg = main.socket.recv(1024).decode()
    print(msg)
















        
