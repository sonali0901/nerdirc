""" Usage:

    This plugin makes spam on a network.
    You just need a router bot which accepts the syntax.
    !carry nick <msg>

    You join some channels and add to constraints all the channels
    which you don't want users to be invited.

    When a user types on the channel it will call the bot router
    to send a msg to the person who typed on the channel.
    and its host is added to WHO.
"""

from tkinter import *
import random

# It avoids sending msg to who is in one of these channels
CONSTRAINT = ['#freenode', '#vy']
DATABASE   = ['Hi. What do you think of this vim-like editir in python? https://github.com/iogf/vy The supposed chan is #vy. there is this video https://www.youtube.com/watch?v=igZWcc-foJg ']

WHO        = []

def ujoin(event, server, view):
    global CONSTRAINT
    global WHO

    chan = event['channel'].lower()
    nick = event['nicka']
    host = event['host']

    if host in WHO: return
    for ind in CONSTRAINT:
        win = view.get_win((server.getName(), ind))

        if win and nick in win.box.get(0, END):
            return

    server.send_msg(nick, random.choice(DATABASE))
    WHO.append(host)


