import lib
import plugins_helper as p


##### START PLUGIN #####

# TITLE: EXAMPLE PLUGIN

# DESCRIPTION: Example plugin!!! By Omena0, Use this to learn the basic ways of my plugin system!

# NAMESPACE: "example"

#### CODE ####

def on_msg(username,msg,ip,cs):
    if msg.startswith('!test_command'):
        cs.send('Hello, world!'.encode())

example = p.plugin()
example.on_msg = on_msg

##### END PLUGIN #####



# PLUGINS LIST: (DISABLE PLUGIN BY NOT ADDING IT)
plugins = [example] # add "logger" to list to enable it, this is not on by default because it serves no real purpose.
