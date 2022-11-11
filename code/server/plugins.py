import lib
import plugins_helper as p

# Note: Please use this template when making plugins, it makes it alot easier!
# I will add more events in like 10 min wait a sec


##### START PLUGIN #####

# TITLE: EXAMPLE PLUGIN

# DESCRIPTION: Example plugin!!! By Omena0, Use this to learn the basic ways of my plugin system!

# NAMESPACE: "p1"

#### CODE ####

# Define functions for events (USE ANY NAME U WANT)
def on_msg(user,msg,ip):
    print(f'MESSAGE FROM {user} at {ip}: {msg}')
def on_join(ip,port):
    print(f'NEW CLIENT FROM {ip}:{port}')
def on_leave(ip,port):
    print(f'CLIENT FROM {ip}:{port} Left!')
def on_init():
    print('EXAMPLE PLUGIN LOADED!')
def on_login(user,ip,port,status):
    print(f'--- USERSTATUS ---\nUser: {user}\nAddress: {ip}:{port}\nStatus: {status}')


# Add the functions u defined earlier to the plugin
p1 = p.plugin()
p1.on_msg = on_msg
p1.on_join = on_join
p1.on_leave = on_leave
p1.on_init = on_init
p1.on_login = on_login

##### END PLUGIN #####



# PLUGINS LIST: (DISABLE PLUGIN BY NOT ADDING IT)
plugins = [] # add p1 to list to enable it, this is not on by default because it server no real purpose.
