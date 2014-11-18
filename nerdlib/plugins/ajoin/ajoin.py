
def ukick(event, server, view):
    chan = event['channel'].lower()
    server.send_cmd('JOIN %s', chan)
        






