# MSG APP V4
 Oh, its another msg app?

It will be done really soon dont worry!!

## NEWS:
TUNNELING SUPPORT!!!
YOU CAN NOW ACTUALLY RUN A SERVER WITHOUT PORT FORWARDING
See tutorial bellow for more

# How to set up the server:

### Download the code/server folder

### Next you will need to set up a tunnel using playit 
 (you can use another tunneling service but playit is really great)
1. Go to [Playit.gg](https://playit.gg/) and create an account.
2. Click Add tunnel
3. Set tunnel type to custom
4. Leave the Local Ipv4 to 127.0.0.1 and set the Local Port to 5000 (see config)
5. Set port type to "TCP" and leave port count to 1
6. Click create tunnel
7. Download the newest version of playit. (As of writing 0.9.3)
8. Run the Playit program
It asks you to sign in again, after that:
In playit.gg (website) look at the tunnel you created.
Take note of the following values:
- IPv4 = \<TUNNEL IP\>
- Port = \<TUNNEL PORT\>

#### Make new file called 'confing.py', and put the following content in it:
```python
# DONT MODIFY IP, PORT, AUTHIP OR AUTHPORT UNLESS YOU KNOW WHAT UR DOING!
ip = '127.0.0.1'
port = 5000

authip = '147.185.221.229'
authport = 49805

# Fill this is for server discovery. 
# If you dont have a server account, the only way for the client to join will be by specifying a custom ip
server_name = '<SERVER NAME>'
server_id = '<SERVER ID>'     
server_password = '<SERVER PASSWORD>'

# Where the auth server will tell the client to connect when joining a server.
# MAKE SURE TO FILL THEESE IN!!!
server_ip = '<TUNNEL IP>'
server_port = <TUNNEL PORT>
```

#### MAKE SURE TO FILL ALL OF THE VALUES IN!

Finally run the playit program (aka agent) and server.py.
If it gives you some over-simplified error msg and doesent close try typing "debug" Then it might give you the actual error message.

Now you can try to connect, if you have a server account you will see the server in server discorvery once its running, but if you dont, heres how to connect:

1. Make sure playit AND the server are running.
2. Open the client.
3. Log in using your username and password (if u want account dm me on discord)
4. When the client asks u to select server type in "c" or "custom" and enter the server_ip and server_port.
5. It should work lul






