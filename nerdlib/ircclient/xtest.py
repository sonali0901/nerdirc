from ircclient.server import *

def initialize():
    x   = Server(server_address = 'irc.brasirc.org', 
                 nick = 'z-alpha', real_name = 'excc', 
                 user_name = 'fc', 
                 port = 6667,
                 server_name = 'freenode')

    x.connect()

    return x

