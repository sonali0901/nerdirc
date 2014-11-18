from threading import *
from socket import *
from queue import *
from nerdlib.ircclient.trigger import *
import os

class Server(Thread):
    MAX_SIZE = 512

    def __init__(self, **args):
        self.server_address = args['server_address']
        self.port = args['port']
        self.server_name = args['server_name']
        self.real_name = args['real_name']
        self.user_name = args['user_name']
        self.nick = args['nick']

        self.charset = args['charset']
        PATH = os.path.dirname(__file__)
        self.trigger_event = Trigger('%s/%s' % (PATH, 'stdevent.txt'))

        self.queue = Queue()
        self.running = False

    def connect(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.start()

        """ test for motd """

    def send_data(self, data):
        if not self.running:
            return

        size = len(data)

        if size > self.MAX_SIZE:
            return

        self.irc_write.write(data)

        self.irc_write.flush()
        
    def send_cmd(self, header, cmd):
        """ Split msg into packeges of 512 bytes """
        """ update self.channel_buffer """
        packet = header % cmd
        data = '%s\r\n' % packet
        self.send_data(data)
        self.enqueue(data)

    def send_msg(self, target, msg):
        self.send_cmd('PRIVMSG %s :%s', (target, msg))
    
    def run(self):
        """ Try to connnect whether something goes wrong it enqueues
            the event onto the queue to be trigged by the client side.
        """

        try:
            self.irc_server = socket(AF_INET, SOCK_STREAM)
            self.irc_server.connect((gethostbyname(self.server_address), self.port))
            self.irc_read = self.irc_server.makefile(mode='rb')
            self.irc_write = self.irc_server.makefile(mode='w')

            self.running = True

            #we first active the thread otherwise 
            #the user ad nick will not be sent

            self.send_cmd("NICK %s", self.nick)
            self.send_cmd('USER %s %s %s :%s', (self.user_name, 'bot1', 'bot2', self.real_name))
        except:
            self.enqueue('FAILED')
            return

        #Notify the plugins it has gone fine
        self.enqueue('SYNCHRONIZED')
        
        self.process()

    def process(self):
        while self.running:
            try:
                raw = self.irc_read.readline()
                data = raw.decode(self.charset)
                self.enqueue(data)

                if not data:
                    break
            except Exception as err:
                print(err)

    def enqueue(self, data):
        """ Here it parses the event and enqueue the respective paramenters/commands """
        trigged = self.trigger_event.matchall(data)
        self.queue.put(trigged)
        #print(dict(trigged))

    def quit(self, msg=''):
        if not self.running:
            return

        self.send_data('QUIT :%s\r\n' %msg)
        self.deactive()
        self.irc_server.close()
        """ I have to see what to do with irc read and irc write """




