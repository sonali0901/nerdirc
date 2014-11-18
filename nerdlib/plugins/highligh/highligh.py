def chmsg(event, server, view):
    bgcolor = ''
    fgcolor = 'blue'

    chan = event['channel'].lower()
    nick = event['nicka']
    msg = event['msg']
    win = view.get_win((server.getName(), chan))
    
    short = ('end -2 char linestart','end -2 char lineend')

    if win.server.nick.lower() in msg.lower():
        for ind in view.obj.values():
            if ind.target == chan:
                ind.text.tag_add('LASTLINE', *short)
                ind.text.tag_config('LASTLINE', 
                                    background=bgcolor, 
                                    foreground=fgcolor)
        


