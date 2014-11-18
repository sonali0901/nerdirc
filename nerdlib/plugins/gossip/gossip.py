
def chmsg(event, server, view):
    chan = event['channel'].lower()
    nick = event['nicka']
    msg = event['msg']
    win = view.get_win((server.getName(), chan))

    if win.server.nick in msg:
        for ind in view.obj.values():
            if ind.target != chan:
                packet = '>>> %s has mentioned your nick on %s <<<\n' % (nick, chan)
                ind.update_screen(packet)
        



