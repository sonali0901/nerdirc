import re
import webbrowser

def start_browser(event, url):
    webbrowser.open(url)


def chmsg(event, server, view):
    chan = event['channel'].lower()

    win = view.get_win((server.getName(), chan))

    mark(win)

def umsg(event, server, view):
    nick = event['nicka'].lower()
    win = view.get_win((server.getName(), nick))
    mark(win)

def lumsg(event, server, view):
    nick = event['target'].lower()
    win = view.get_win((server.getName(), nick))
    mark(win)

def lchmsg(event, server, view):
    nick = event['target'].lower()
    win = view.get_win((server.getName(), nick))
    mark(win)

def utopic(event, server, view):
    chan = event['channel'].lower()

    win = view.get_win((server.getName(), chan))

    mark(win)

def ukick(event, server, view):
    chan = event['channel'].lower()

    win = view.get_win((server.getName(), chan))

    mark(win)

def userv(event, server, view):
    win = view.get_win(server.getName())

    mark(win)

def mark(win):
    bgcolor = ''
    fgcolor= 'red'
    ul=True

    msg = win.text.get('end -2 char linestart', 'end -2 char lineend')

    regex = '(?P<addr>http[s]?://[^ ]*)'

    seq = re.finditer(regex, msg)

    if not seq:
        return


    for obj in seq:
        posx = 'end -2 lines linestart +%s char' % obj.start()  
        posy = 'end -2 lines linestart +%s char' % (obj.end() + 1)
        
        win.text.tag_add(obj.group('addr'), posx, posy)

        win.text.tag_config(obj.group('addr'), 
                            background=bgcolor,
                            foreground=fgcolor,
                            underline=ul)

        win.text.tag_bind(obj.group('addr'), 
                          '<Double-Button-1>',  
                          lambda event, url=obj.group('addr'): start_browser(event, url))



