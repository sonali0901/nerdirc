from nerdlib.user import *
from nerdlib.channel import *

bgcolor = ''
fgcolor = 'brown'

def chmsg(event, server, view):
    chan = event['channel'].lower()
    nicka = event['nicka']

    win = view.get_win((server.getName(), chan))
    attach_tag(win, nicka, view)

def ukick(event, server, view):
    chan = event['channel'].lower()
    nickb = event['nickb']

    win = view.get_win((server.getName(), chan))

    attach_tag(win, nickb, view)

def chnick(event, server, view):
    nicka = event['nicka']
    nickb = event['nickb']

    for key, value in view.obj.items():
        if not isinstance(value, Channel):
            continue

        #If the server isn't the same then continues.
        #Notice, all servers are indexed in the same list
        if not value.server == server:
            continue

        group = value.box.get(0, END) 

        if nickb in group:
            attach_tag(value, nickb, view)

def ujoin(event, server, view):
    nicka = event['nicka']
    chan = event['channel'].lower()
    win = view.get_win((server.getName(), chan))

    attach_tag(win, nicka, view)

def upart(event, server, view):
    """ It does alike ujoin except it works with part.
        If the nick corresponds to the own user then
    """

    nicka = event['nicka']
    chan = event['channel'].lower()
    win = view.get_win((server.getName(), chan))

    #this might throw an exception
    #if you are the one leaving
    #it will just break the execution which is fine here
    attach_tag(win, nicka, view)

def attach_tag(win, nick, view):
    msg = win.text.get('end -2 char linestart', 'end -2 char lineend')
    print(msg)

    start = msg.index(nick)
    end = start + len(nick)

    posx = 'end -2 lines linestart +%s char' % start 
    posy = 'end -2 lines linestart +%s char' % end
    
    win.text.tag_add(nick.lower(), posx, posy)

    win.text.tag_config(nick.lower(), 
                        background=bgcolor,
                        foreground=fgcolor,
                        underline=True)

    win.text.tag_bind(nick.lower(), 
                      '<Double-Button-1>',  lambda event, a=win, b=nick, c=view: open_pvt(a, b, c))

def open_pvt(win, nick, view):
    if view.get_win((win.server.getName(), nick.lower())):
        return

    wuser = User(win.server, nick)

    view.add_win(wuser, 
                      win.server.getName(), 
                      'end', 
                      (win.server.getName(), nick.lower()), 
                      text=nick)



