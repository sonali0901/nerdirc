from nerdlib.user import User


def lquery(event, server, view, peerwin):
    nick = event['nick']
    print(view)
    win = view.get_win((server.getName(), nick.lower()))
    if not win:
        uwin = User(server,
                    nick,
                    master=view)
        view.add_win(uwin, 
                     server.getName(), 
                     'end', 
                     (server.getName(), nick.lower()), 
                     text=nick)

# Define a shortcut for /query.  
lq = lquery

def lpart(event, server, view, peerwin):
    server.send_data('PART %s\r\n' % peerwin.target)

lp = lpart

def lmsg(event, server, view, peerwin):
    target = event['target']
    msg = event['msg']
    server.send_data('PRIVMSG %s :%s\r\n' % (target, msg))

def lj(event, server, view, peerwin):
    target = event['target']
    server.send_data('JOIN %s\r\n' % target)


