def chmsg(event, server, view):
    """ Everytime someone types on a channel this method is called 
        It gets the channel name and the win(that one which we have added in the ujoin event.
        It gets the window with the same method server.getName.
    """

    ch = event['channel'].lower()
    win = view.get_win((server.getName(), ch))

    msg = event['msg']

    if server.nick in msg:
        win.update()
        win.deiconify()
