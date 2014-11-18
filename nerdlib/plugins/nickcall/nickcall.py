def chmsg(event, server, view):
    chan = event['channel'].lower()
    nick = event['nicka']
    msg = event['msg']
    index = (server.getName(), chan)
    win = view.get_win(index)
  
    if win.server.nick.lower() in msg.lower() and win.state() != 'normal':
        index = str(index)
        tagind = index.replace(' ', '_')
        view.item(index, tags=tagind)

        def uncolor(seq_event, tagind=tagind):
            seq_event.widget.tag_configure(tagind, foreground='black')
            seq_event.widget.item(index, tags='')

        view.tag_bind(tagind, '<Double-Button-1>', uncolor)
        view.tag_configure(tagind, foreground='blue')
        

def umsg(event, server, view):
    nicka = event['nicka'].lower()
    index = (server.getName(), nicka)
    win = view.get_win(index)
  
    if win.state() != 'normal':
        index = str(index)
        tagind = index.replace(' ', '_')
        view.item(index, tags=tagind)

        def uncolor(seq_event, tagind=tagind):
            seq_event.widget.tag_configure(tagind, foreground='black')
            seq_event.widget.item(index, tags='')

        view.tag_bind(tagind, '<Double-Button-1>', uncolor)
        view.tag_configure(tagind, foreground='red')



