if __name__ == '__main__':
    exit('Do not run the library! Import it!')


global hasInit
hasInit = False

import rsa
publicKey, privateKey = rsa.newkeys(512)

users = []
names = []
passwords = []
import time as t
import random as r
import hashlib as h


version = 'V0.06.5'

global currentuser



def init(versionMessage=True):

    global hasInit
    hasInit = True
    VMsg = versionMessage
    if VMsg == True:
        log('ABOUT',f'You are using Omena0\'s utilib {version}. \nTo disable this message add \'versionMessage=False\' to the init() args.')
    
def about():
    log('ABOUT',f'You are using Omena0\'s utilib {version}!')

def hash(value):
    return h.sha1(str(value).encode()).hexdigest()


def encrypt(data,publicKey=publicKey):
    return rsa.encrypt(data.encode(),publicKey)

def decrypt(data,privateKey=privateKey):
    return rsa.decrypt(data,privateKey).decode()
    
def debug():
    init(versionMessage=False)
    
def rand(num1,num2):
    return r.randrange(num1,num2)
            
def time():
    return t.strftime('%H:%m:%S')
        
def log(type,msg):
    print(f'[{type}]: {time()} > - {msg}')
    
def packetlog(outgoing,msg):
    if outgoing:
        print(f'\n{time()} OUT>>> {msg}')
    else: print(f'\n{time()} <<<<IN {msg}')
    
def sign(data,publicKey=publicKey):
    return [str(data), encrypt(data,publicKey)]

def verify(data,privateKey=privateKey):
    return data[0] == decrypt(data[1],privateKey)


class user:
    def __init__(self,username,psw):
        while username in names:
            username = username + '#'
        self.username = username
        self.psw = psw
        names.append(username)
        
    def __str__(self):
        return str(self.username)
    def bind(self,name,value):
        exec(f'self.{name} = {value}')
    
def adduser(name,psw):
    if name in names:
        return False
    name = str(name)
    psw = str(psw)
    newuser = user(name,psw)
    users.append(newuser)
    passwords.append(psw)
    
    
def userStr():
    userStr = ''
    index = 0
    for i in users:
        userStr = userStr + str(names[index]) + ', '
        index =+1
    return userStr

def userindex(target):
    if target in names:
        index = 0
        for i in names:
            if names[index] == target:
                return int(index)
            else: index =+ 1
        return -1
    else:
        return -1
        
    
def pswcheck(target,test):
    if str(users[userindex(target)].psw) == str(test):
        return True
    else: return False
    

def login(name=None,psw=None):
    global currentuser
    if name not in names:
        return 0
    if psw == users[userindex(name)].psw:
        currentuser = name
        return 1
    else: return -1


                
            
 
        
