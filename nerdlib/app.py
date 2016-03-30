from tkinter import *
from tkinter import ttk
from nerdlib.manager import Manager
from nerdlib.user import User
from nerdlib.ircclient.hold import *
from nerdlib.ircclient.dispatcher import *
from nerdlib.askstring import *
from nerdlib.selserver import *
from nerdlib.selstyle import *
from nerdlib.selplugin import *
from nerdlib.channel import *
from tkinter import messagebox
from nerdlib.dccsend import *
from os.path import getsize
import os

HEADER = '\001DCC SEND %s %s %s %s\001' 

class Nerd(object):
    def __init__(self, root):
        self.root = root
        self.root.title('Nerdirc')

        self.main = ttk.Frame(relief=RAISED,
                              padding=(3, 3),
                              border=3)
        
        self.scrollbar = ttk.Scrollbar(master=self.main)

        self.view = Manager(self.main, yscrollcommand=self.scrollbar.set)
        self.view.heading('#0', text='Server')
        
        self.scrollbar.config(command=self.view.yview)
        self.scrollbar.pack(side='right', fill=Y)

        self.view.pack(side='top', expand=True, fill=BOTH)


        self.buttonbox = ttk.Frame(self.root,
                                   relief = RAISED,
                                   padding=(3, 3),
                                   border=3)

   
        PATH = os.path.dirname(__file__)
        self.img1 = PhotoImage(file='%s/%s' % (PATH, 'icon/plug.gif'))

        self.img2 = PhotoImage(file='%s/%s' % (PATH,'icon/delete.gif'))
        self.img3 = PhotoImage(file='%s/%s' % (PATH,'icon/users.gif'))
        self.img4 = PhotoImage(file='%s/%s' % (PATH,'icon/user.gif'))

        self.img5 = PhotoImage(file='%s/%s' % (PATH,'icon/help.gif'))
        self.img6 = PhotoImage(file='%s/%s' % (PATH,'icon/sendfile.gif'))
        self.img7 = PhotoImage(file='%s/%s' % (PATH,'icon/exit.gif'))
        self.img8 = PhotoImage(file='%s/%s' % (PATH,'icon/hammer.gif'))
        self.img9 = PhotoImage(file='%s/%s' % (PATH,'icon/style.gif'))

        self.button1 = Button(self.buttonbox, image=self.img1, command=self.new_server) 
        self.button2 = Button(self.buttonbox, image=self.img2, command=self.kill)
        self.button3 = Button(self.buttonbox, image=self.img3, command=self.join_channel)
        self.button4 = Button(self.buttonbox, image=self.img4, command=self.open_pvt)
        self.button5 = Button(self.buttonbox, image=self.img5, command=self.about)
        self.button6 = Button(self.buttonbox, image=self.img6, command=self.send_file)
        self.button7 = Button(self.buttonbox, image=self.img7, command=self.root.quit)
        self.button8 = Button(self.buttonbox, image=self.img8, command=self.config)
        self.button9 = Button(self.buttonbox, image=self.img9, command=lambda :SelectStyle(self.root))
        
        self.button1.grid(row=0, column=0)
        self.button2.grid(row=0, column=1)
        self.button3.grid(row=0, column=2)
        self.button4.grid(row=0, column=3)
        self.button5.grid(row=0, column=4)
        self.button6.grid(row=0, column=5)
        self.button7.grid(row=0, column=6)
        self.button8.grid(row=0, column=7)
        self.button9.grid(row=0, column=8)

        self.root.bind('<Escape>', lambda widget: self.root.iconify())
        self.root.bind('<KeyPress-F1>', lambda widget: self.join_channel())
        self.root.bind('<KeyPress-F2>', lambda widget: self.open_pvt())

        self.buttonbox.pack(side='bottom', fill=BOTH)

        self.main.pack(expand=True, fill=BOTH)

        from nerdlib.config import initialize

        filename = initialize()
        self.config = shelve.open(filename, writeback=True)

        plugins = self.config['plugins']
        self.config.close()

        self.hold = Hold(*plugins)

        self.dispatcher = Dispatcher(self.hold, self.view)
        self.process()

    def config(self):
        SelectPlugin(self.root)

    def send_file(self):
        choice = self.view.selection()[0]
        win = self.view.get_win(choice)


        nick = AskString(self.root, 'Nick', 'Nick').result

        if not nick:
            return

        port = AskString(self.root, 'Port', 'Port').result

        if not port:
            return

        filename = filedialog.askopenfilename() 

        if not filename:
            return

        size = getsize(filename)

        request = HEADER % (filename.rsplit('/', 1)[1], 
                            ip_to_long(win.server.myaddr), 
                            port, 
                            size)
        
        DccSend(nick, filename, port)

        win.server.send_data('PRIVMSG %s :%s\r\n' %  (nick, request)) 

    def process(self):
        PERIOD = 200
        self.root.after(PERIOD, self.process)
        self.dispatcher.dispatch()

    def new_server(self):
        selectserver = SelectServer(self.root)
        info = selectserver.get_info()

        if not info:
            return

        self.hold.new_server(server_name=info[5],
                             server_address=info[0],
                             real_name=info[1],
                             nick=info[2],
                             user_name=info[3],
                             port=info[4],
                             charset=info[6])

    def join_channel(self):
        channel = AskString(self.root, 'Channel', 'Channel').result

        if not channel:
            return

        choice = self.view.selection()[0]
        win = self.view.get_win(choice)

        win.server.send_cmd('JOIN %s', channel)


    def open_pvt(self):
        nick = AskString(self.root, 'Nick', 'Nick').result

        if not nick:
            return

        choice = self.view.selection()[0]

        win = self.view.get_win(choice)

        if self.view.get_win((win.server.getName(), nick.lower())):
            return

        wuser = User(win.server, nick)

        self.view.add_win(wuser, 
                          win.server.getName(), 
                          'end', 
                          (win.server.getName(), nick.lower()), 
                          text=nick)

    def kill(self):
        choice = self.view.selection()[0]
        win = self.view.get_win(choice)

        if isinstance(win, Channel):
            win.server.send_cmd('PART %s', win.target)
        elif not self.view.parent(choice):
            #Should ask for a quit msg
            win.server.send_cmd('quit :%s', 'Nerdirc is the script. Pick up yours !')
        else:
            self.view.del_win(choice)

    def about(self):
        messagebox.showinfo('About', 
                'Author:Iury O. G. Figueiredo\nNick:Tau\nE-mail:robatsch@hotmail.com')

















