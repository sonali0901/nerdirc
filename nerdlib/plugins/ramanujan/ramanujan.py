import re
import random
import time

def chmsg(event, server, view):
    ch = event['channel'].lower()

    win = view.get_win((server.getName(), ch))

    msg = event['msg']

    exp = ''.join(re.findall('[0-9*-+/^]', msg))

    if not exp:
        return

    over = re.findall('[0-9]+', exp)

    for ind in over:
        if int(ind) > 10 ** 3:
            return

    answer = eval(exp)

    """
    if answer > 15000:
        return
    """

    win.update_screen('<%s>%s\n' % (server.nick, answer))

    #time.sleep(random.randint(2, 4))
    server.send_msg(ch, answer)


