import socket
import lib
from threading import Thread

authip = '127.0.0.1'
authport = 5001

print('Log in to continue:')

name = input('Username: ')
psw = input('Password: ')

main = socket.socket()

auth = socket.socket()
auth.connect((authip,authport))
result = ''
auth.send(f'GET-SERVERS'.encode())
servers = auth.recv(1024).decode().split(':') # RAW: ['Another test server,OFFLINE,OFFLINE', 'A test server,OFFLINE,OFFLINE', '']
for server in enumerate(servers):
    index = server[0]
    server = server[1]
    if server == '': continue
    server = server.split(',')
    result = f'-- SERVER --\nINDEX: {index}\nNAME: "{server[0]}"\nIP: {server[1]}\nPORT: {server[2]}\n\n{result}'
print('--- PUBLIC SERVERS ---\n')
print(result)
print(servers)

ip = 'OFFLINE'
port = 'OFFLINE'

while ip == 'OFFLINE':
    try: a = int(input('Choose server:'))
    except:
        print('Please enter a number.')
        continue
    if a > len(servers)-2: print(f'Out of range. Accepted range is 0-{len(servers)-2}')
    for server in enumerate(servers):
        index = server[0]
        server = server[1]
        if server == '': continue
        if index == int(a):
            server = server.split(',')
            ip = server[1]
            port = server[2]
            if ip == 'OFFLINE':
                print('server.py')




    
auth.send(f'GET-TOKEN {name}:{lib.hash(psw)}'.encode())

msg = auth.recv(2048).decode()
if msg.startswith('X_'):
    lib.log('ERROR',msg)
token = msg # + ' INVALIDATE-TOKEN' # Toggle on when testing for invalid token


main.connect((ip,int(port)))

def listener():
    while True:
        msg = ''
        try: msg = main.recv(1024).decode()
        except: lib.log('!','The connection was closed due to an error or you were kicked from the server (check auth)')
        if msg.startswith('[MESSAGE]'):
            msg = msg.split('<END>')[0].replace('[MESSAGE]','').split('<SEP>')
            lib.log('MSG',f'{msg[0]} > {msg[1]}\n')
        
        
lib.log('*','Logged in as {name}.')
        

        

a = Thread(target=listener)
a.daemon = True
a.start()

lib.log('*','Type and hit enter to send message.')

while True:
    msg = input()
    main.send(f'{msg} <SEP>{token}'.encode())
    

while True: pass
