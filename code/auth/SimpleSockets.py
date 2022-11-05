def stop():
    while True: pass
    exit('No thanks ;)')


import lib
import socket
import os
import sys
from threading import Thread




class connection:
    def default(self,a,b,c): pass
    def __init__(self,ip,port,type,logging=False,msgbits=1024):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.type = type
        self.logging = logging
        self.clients = set()
        self.msgbits = msgbits
        
        self._on_connect = self.default
        self._on_disconnect = self.default
        self._on_msg = self.default
        
        if not type in ['server','client']: type = 'client'
        if type == 'client':
            try: self.socket.connect((ip,port))
            except OSError:
                print(f'[!] Connection failed! Target machine is not listening on port {self.port} [OSError]')
        if type == 'server':
            try: self.socket.bind((ip,port))
            except socket.gaierror:
                print('[!] Bind failed! Ip address is invalid! [socket.gaierror]')
                stop()
            except OSError:
                print('[!] Bind failed! Ip address is not valid in its context! [OSError]')
                stop()
            self.socket.listen(5)
            if self.logging: lib.log('*',f'Listening on {self.ip}:{self.port}')
            listener = Thread(target=self._listen)
            listener.daemon = True
            listener.start()
            if self.logging: lib.log('*','Listener started! You can now connect.')

    def _handle_client(self,cs,address):
        while True:
            try: msg = cs.recv(self.msgbits).decode()
            except:
                try:
                    self._on_disconnect(cs,address[0],address[1])
                    self.clients.remove(cs)
                    cs.close()
                    break
                except: break
            self._on_msg(msg,cs,address)
    
    def _listen(self):
        while True:
            cs, address = self.socket.accept()
            self._on_connect(cs,address[0],address[1])
            self.clients.add(cs)
            a = Thread(target=self._handle_client,args=[cs,address])
            a.daemon = True
            a.start()
            
    def send(self,msg):
        if self.type == 'client':
            self.socket.send(msg.encode())
        if self.type == 'server':
            for cs in self.clients:
                cs.send(msg.encode())
    def bind(self,event,function):
        if event == 'connect':
            self._on_connect = function
        if event == 'disconnect':
            self._on_disconnect = function
        if event == 'msg':
            self._on_msg = function
        else:
            exec(f'self.{event} = "{function}"')
