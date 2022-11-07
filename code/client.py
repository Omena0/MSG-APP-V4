import socket
import lib
from threading import Thread

ip = '127.0.0.1'
port = 5000

authip = '127.0.0.1'
authport = 5001

name = 'Omena0'
psw = '1234'

s = socket.socket()
s.connect((authip,authport))
s.send(f'GET-TOKEN {name}:{lib.hash(psw)}'.encode())
while True:
    msg = s.recv(1024).decode()
    if msg.startswith('X_'):
        lib.log('ERROR',msg)
        break
    token = msg
    break
s = socket.socket()
s.connect((ip,port))

def listener():
    while True:
        msg = s.recv(1024).decode()
        if msg.startswith('[MSG] '):
            msg = msg.replace('[MSG] ','').split('<SEP>')
            lib.log('MSG',f'{msg[0]} > {msg[1]}')
        
        
        
        
        
        

a = Thread(target=listener)
a.daemon = True
a.start()

while True:
    msg = input()
    s.send(f'{msg}<SEP>{token}'.encode())
    





while True: pass









