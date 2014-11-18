from trigger import *
x = Trigger('stdevent.txt')
print(list(x.matchall(':ee!~fff@186-194-34-25.i-next.psi.br PRIVMSG uuuu :DCC SEND postal2 3133284889 45949 151\r\n')))
