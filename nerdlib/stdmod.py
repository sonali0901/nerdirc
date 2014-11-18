""" This file holds all methods which perform actions based on irc server events."""

from tkinter import *
from nerdlib.channel import *
from nerdlib.user import *
from tkinter.messagebox import showerror
from nerdlib.dccget import *
import nerdlib.config
import re
from tkinter import filedialog
MODE = '@+'

def usync(event, server, view):
    """ This method is called when a connection goes fine.
        So, it creates a new window to serve as main window for the server.
        It passes the server instance to it, since it will use the server instance
        to send data to the server.
        It gets the server name via getName method which comes from Thread class.
        It does so to index the server instance inside Manager class instance.
    """
    wserv = User(server, server.server_address, view)
    view.add_win(wserv, '', 'end', server.getName(), text=wserv.target)

def dccsend(event, server, view):
    showinfo('Dcc', '%s wants to send %s, size:%s' % (event['nicka'],event['file'], event['size']))
    filename = filedialog.asksaveasfilename()

    if filename:
        DccGet(event['nicka'], event['ip'], filename, int(event['size']), event['port'])
        

def motd(event, server, view):
    server.send_cmd('userhost %s', server.nick) 
    server.nick = event['nicka']

def userhost(event, server, view):
    server.myaddr = event['myaddr']

def ufailed(event, server, view):
    """ If a connection attempt has failed then it is called """
    showerror('Error', 'Impossible to connect !')
    pass

def chmsg(event, server, view):
    """ Everytime someone types on a channel this method is called 
        It gets the channel name and the win(that one which we have added in the ujoin event.
        It gets the window with the same method server.getName.
    """

    ch = event['channel'].lower()
    win = view.get_win((server.getName(), ch))

    nicka = event['nicka']
    msg = event['msg']

    packet = '<%s>%s\n' % (nicka, msg)

    win.update_screen(packet)

def userv(event, server, view):
    """ This method is called everytime some data comes from the irc server.
        There is a regex meaning it in the stdevent.txt
    """

    data = event['data']
    packet = '%s\n' % data
    win = view.get_win(server.getName())

    win.update_screen(packet)

def ping(event, server, view):
    """ If some ping occured then replies to it """
    server.send_cmd('PONG :%s', event['server'])
    print('PONG PING')

def ukick(event, server, view):
    """ If some user has been kicked then it performs the task
        of getting rid of the nick from the channel listbox
        if it is the own user then it removes the window
    """

    nick = event['nickb']
    msg = event['msg']
    chan = event['channel'].lower()
    win = view.get_win((server.getName(), chan))

    packet = '%s has been kicked %s :%s\n' % (nick, chan, msg)

    group = win.box.get(0, END)
    ind = group.index(nick)

    win.box.delete(ind)
    win.update_screen(packet)

    #If it is the own user then removes the window
    if nick == server.nick:
        view.del_win((server.getName(), chan))


def umode(event, server, view):
    """ This method is called everytime someone sets mode on a nick.
        It uses colours instead of @ and +.
    """

    nicka = event['nicka']
    nickb = event['nickb']
    mode = event['mode']
    chan = event['channel'].lower()

    #As usual getting the window corresponding to the channel
    win = view.get_win((server.getName(), chan))

    packet = '%s sets mode %s on %s\n' % (nicka, mode, nickb)

    #Updating the screen
    win.update_screen(packet)

    #If mode is not in the tuple then it is not needed to bother with its color
    if not mode in ('+o', '-o', '+v', '-v'):
        return

    #Get the list of nicks
    group = win.box.get(0, 'end')

    #Get the position of the nick
    ind = group.index(nickb)


    #Update the new nick state
    if mode == '+o':
       win.box.itemconfigure(ind, background='brown')
    elif mode == '-o':
        win.box.itemconfigure(ind, background='')
    elif mode == '+v':
        win.box.itemconfigure(ind, foreground='green')
    elif mode == '-v':
        win.box.itemconfigure(ind, foreground='')


def utopic(event, server, view):
    """ When it joins a channel this method is called if the channel
        has a topic.
    """
    chan = event['channel'].lower()
    topic = event['topic']

    #Getting the window which corresponds to the channel
    win = view.get_win((server.getName(), chan))

    packet = '%s topic: %s\n' % (chan, topic)
    win.update_screen(packet)

def utsb(event, server, view):
    """ This method is called to set who has set the topic"""
    chan = event['channel'].lower()
    nickb = event['nickb']
    win = view.get_win((server.getName(), chan))

    packet = 'Topic on %s set by %s\n' % (chan, nickb)
    win.update_screen(packet)

def ugroup(event, server, view):
    """ This method is called with the list nicks for who is in the channel"""
    group = event['group'].split(' ')
    chan = event['channel'].lower()
    win = view.get_win((server.getName(), chan))

    #It sets background and foreground for a given state @ and +
    for ind in group:
        win.box.insert(END, ind.strip(MODE))
        if ind.startswith('+'):
            win.box.itemconfigure(END, foreground='green')
        elif ind.startswith('@'):
            win.box.itemconfigure(END, background='brown')

def ujoin(event, server, view):
    """ If someone joined the channel or whether you just joined a new channel
        this method updates the channel window or add a new window to the
        view instance
    """
    nick = event['nicka']
    chan = event['channel'].lower()

    packet = '%s has joined %s\n' % (nick, chan)

    try:
        win = view.get_win((server.getName(), chan))
        group = win.box.get(0, END)

        win.box.insert(END, nick) 
        win.update_screen(packet)
    except:
        chwin = Channel(server,
                        chan, 
                        view,
                        master=view)

        view.add_win(chwin, server.getName(), 'end', (server.getName(), chan), text=chan)
        chwin.update_screen(packet)

def upart(event, server, view):
    """ It does alike ujoin except it works with part.
        If the nick corresponds to the own user then
    """

    nick = event['nicka']
    chan = event['channel'].lower()
    win = view.get_win((server.getName(), chan))

    packet = '%s has left %s\n' % (nick, chan)

    group = win.box.get(0, END)
    ind = group.index(nick)

    win.box.delete(ind) 
    win.update_screen(packet)

    if nick == server.nick:
        view.del_win((server.getName(), chan))

def umsg(event, server, view):
    """ Everytime someone sends a private msg it creates a new window
        to talk directly to the user.
    """
    nicka = event['nicka']
    msg = event['msg']

    packet = '<%s>%s\n' % (nicka, msg)

    try:
        win = view.get_win((server.getName(), nicka.lower()))
        win.update_screen(packet)
    except:
        uwin = User(server,
                    nicka,
                    view, 
                    master=view)
        uwin.withdraw()
        view.add_win(uwin, 
                     server.getName(), 
                     'end', 
                     (server.getName(), nicka.lower()), 
                     text=nicka)

        uwin.update_screen(packet)


def uerror(event, server, view):
    """ Error event """
    print('uerror:%s' % event['msg'])

def chnick(event, server, view):
    """ When someone changes its nick.
        if it is the own user then it changes the nick in the server instance.
    """

    nicka = event['nicka']
    nickb = event['nickb']

    packet = '%s changes nick to %s\n' % (nicka, nickb)

    for key, value in view.obj.items():
        if not isinstance(value, Channel):
            continue

        #If the server isn't the same then continues.
        #Notice, all servers are indexed in the same list
        if not value.server == server:
            continue

        try:
            group = value.box.get(0, END)
            ind = group.index(nicka)

            modeX = value.box.itemcget(ind, 'background')
            modeY = value.box.itemcget(ind, 'foreground')

            value.box.delete(ind)
            value.box.insert(ind, nickb)
            value.box.itemconfigure(ind, background=modeX, foreground=modeY)
            value.update_screen(packet)
        except Exception as err:
            print(err)

    if nicka == server.nick:
        server.nick = nickb


def lumsg(event, server, view):
    """ When a private msg is sent """
    target = event['target']
    msg = event['msg']
    pass

def lchmsg(event, server, view):
    """ When a msg on a channel is sent """
    target = event['target']
    msg = event['msg']
    print(target, msg)

def lquit(event, server, view):
    """ When the quit command is sent """
    pass

def llost(event, server, view):
    """ When a connection is lost this method is called to clean up the view instance
        for the given server.
    """
    showerror('Connection lost', 'The connection to the server was lost !')
    view.del_win(server.getName())

def uquit(event, server, view):
    """ When someone quits it updates the channel list box for 
        which the user is in 
    """
    nick = event['nicka']
    msg = event['msg']
           
    packet = '%s has quit %s\n' % (nick, msg)

    for key, value in view.obj.items():
        if not value.server == server:
            continue

        try:
            group = value.box.get(0, END)
            ind = group.index(nick)
            value.box.delete(ind)
        except Exception as err:
            print(err)
            #This structure is possible since
            #Nicks will not start with #
            if not value.target == nick:
                continue

        value.update_screen(packet)








