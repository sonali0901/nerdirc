""" Server name here should be in lower case """
import os
import shelve
from nerdlib.config import initialize

def motd(event, server, view):
    filename = initialize()
    config = shelve.open(filename, writeback=True)

    name = server.server_name.lower()
    for ind in config['server_list']:
        if ind[5].lower() == name:
            for indj in ind[-1]:
                server.send_data('%s\r\n' % indj)
    config.close()










