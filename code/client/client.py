import socket
import lib
from threading import Thread
from getpass import getpass

authip = '147.185.221.229'
authport = 49805

main = socket.socket()
auth = socket.socket()

try:
    auth.connect((authip,authport))
except Exception as e:
    print(f'Could not connect to the Authentication server.')
    offline = True
else: offline = False

if offline: print('You are in OFFLINE MODE! \nYou can only connect to servers that are also in offline mode.\n')
else: print('Log in to continue:')

name = input('Username: ')
if not offline:
    psw = getpass('Password:')
    auth.send(f'GET-TOKEN {name}:{lib.hash(psw)}'.encode())
    msg = auth.recv(2048).decode()
    if msg.startswith('X_'):
        lib.log('ERROR',msg)
    token = msg # + ' INVALIDATE-TOKEN' # Toggle on when testing for invalid token
else: token = f'{name}<TOKEN>OFFLINE'

if not offline:
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
    if not offline:
        a = input('Choose server:')
        if a.lower() == 'c' or a.lower() == 'custom':
            ip = input('IP: ')
            port = input('PORT: ')
            try: port = int(port)
            except:
                print('Please enter a number.')
                while True: pass
            break
    try: a = int(a)
    except:
        print('The port must be a number!')
        continue
    if not offline:
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
                    print('Server is offline!')



main.connect((ip,int(port)))

def listener():
    while True:
        msg = ''
        try: msg = main.recv(1024).decode()
        except Exception as e:
            lib.log('!','The connection was closed due to an error or you were kicked from the server (check auth)')
            if input('') == 'debug': print(f'\n{e}\n')
        if msg.startswith('[MESSAGE]'):
            msg = msg.split('<END>')[0].replace('[MESSAGE]','').split('<SEP>')
            lib.log('MSG',f'{msg[0]} > {msg[1]}\n')
        
        
lib.log('*',f'Logged in as {name}.')
        

        

a = Thread(target=listener)
a.daemon = True
a.start()

lib.log('*','Type and hit enter to send message.')

while True:
    msg = input()
    main.send(f'{msg} <SEP>{token}'.encode())
    

while True: pass
