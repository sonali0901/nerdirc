from tkinter import *
import re
import os
from nerdlib.plugins.latex import tex

database = []
tex = tex.Tex()

def display(win, msg):
    global database
    global tex
    global env

    latex = list(tex.extract(msg))

    if not latex:
        return

    text = win.text

    text.insert(END, '\n')

    for ind in latex:
        eq = PhotoImage(file=ind)
        database.append(eq)

        text.image_create(END, image=database[-1])

        text.insert(END, '  ')

    text.insert(END, '\n\n')
    text.yview(MOVETO, 1.0)


def lchmsg(event, server, view):
    chan = event['target'].lower()
    msg = event['msg']
    win = view.get_win((server.getName(), chan))

    display(win, msg)

def chmsg(event, server, view):
    chan = event['channel'].lower()
    msg = event['msg']
    win = view.get_win((server.getName(), chan))

    display(win, msg)




