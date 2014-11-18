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

#The bot
from tkinter import *
import random

BOT = 'Quadrescense'

#It avoids sending msg to who is in one of these channels
CONSTRAINT = ['#calculus', '#freenode', '#guppy', '##blackhats', '#untwisted']

DATABASE = ['Hello. Could you join #calculus and ask them to unban me?',
            'Hello, Could you join calculus and ask them how can i calculate x^2? i am banned',
            'Join #calculus and ask somebody to unban me. please',
            'I need you to join #calculus and ask them a question for me. it is a math channel']

WHO = []

def chmsg(event, server, view):
    global BOT
    global CONSTRAINT
    global WHO

    chan = event['channel'].lower()
    nick = event['nicka']
    host = event['host']

    if host in WHO:
        return

    for ind in CONSTRAINT:
        win = view.get_win((server.getName(), ind))

        if win:
            if nick in win.box.get(0, END):
                return

    phrase = random.choice(DATABASE) 

    server.send_msg(BOT, '!carry %s <%s>' % (nick, phrase))

    WHO.append(host)

