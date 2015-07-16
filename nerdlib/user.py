from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from nerdlib.utils import ircwrap
from nerdlib.ircclient.module import *
from nerdlib.ircclient.trigger import *
import shelve
import os
from nerdlib.config import initialize

class User(Toplevel):
    DELIMITER = '/'
    LENGTH = 512
    
    def __init__(self, 
                 server=None,
                 target=None,
                 view=None,
                 *args, 
                 **kwargs):

        Toplevel.__init__(self, *args, **kwargs)

        self.server=server
        self.target = target
        self.title(target)
        self.view = view
        self.menubar = Menu(master=self)

        self.usermenu = Menu(self.menubar, tearoff = 0) 
   
        self.usermenu.add_command(label='Save buffer', command = self.save_buffer)
        self.usermenu.add_separator()
        self.usermenu.add_command(label='Close', command = self.withdraw)
        self.menubar.add_cascade(label='User', menu=self.usermenu)

        self.config(menu=self.menubar)

        self.top = ttk.Frame(self,
                          relief = RAISED,
                          padding=(3, 3),
                          border=3)

    

        self.scrollbar = ttk.Scrollbar(master=self.top)

        filename = initialize()
        self.config = shelve.open(filename, writeback=True)

        text_theme = self.config['text_theme']

        self.text = Text(master=self.top, 
                         yscrollcommand=self.scrollbar.set,
                         **text_theme)


        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(side='right', fill=Y)

        self.down = ttk.Frame(self,
                          relief = RAISED,
                          padding=(3, 3),
                          border=3)



        entry_theme = self.config['text_theme']
        self.entry = Entry(master=self.down, **entry_theme)
        self.entry.pack(fill=X)
        self.entry.focus_set()

        self.text.pack(side='left', expand=True, fill=BOTH)
        self.down.pack(side='bottom', fill=X)
        self.top.pack(side='top', expand=True,fill=BOTH)
       
        self.entry.bind('<KeyPress-Return>', self.send)
        self.entry.bind('<KP_Enter>', self.send)


        self.popup = Menu(self.entry, tearoff = 0)

        self.popup.add_command(label="Copy")

        self.popup.add_command(label="Cut")

        self.popup.add_command(label="Paste")

        self.popup.add_command(label="Select all")

        self.entry.bind('<Button-3>', self.post_popup)

        self.text.bind('<Button-3>', self.post_popup)

        self.protocol('WM_TAKE_FOCUS', self.entry.focus_set)

    def save_buffer(self):
        f = tkFileDialog.asksaveasfilename()

        if not f:
            return

        out = open(f, 'w')
        out.write(self.text.get('1.0', END))
        out.close()

    def post_popup(self, event):
        widget = event.widget

        self.popup.entryconfigure('Cut', command = lambda: 
                                                widget.event_generate('<<Cut>>'))

        self.popup.entryconfigure('Copy', command = lambda: 
                                                widget.event_generate('<<Copy>>'))

        self.popup.entryconfigure('Paste', command = lambda: 
                                                widget.event_generate('<<Paste>>'))

        self.popup.entryconfigure('Select all', command = lambda: 
                                                widget.event_generate('<<Select All>>'))

        self.popup.tk_popup(event.x_root, event.y_root, 0)

    def save_buffer(self):
        f = filedialog.asksaveasfilename()

        if not f:
            return

        out = open(f, 'w')
        out.write(self.text.get('1.0', END))
        out.close()

    def update_screen(self, msg):
        self.text.insert(END, msg)
        self.text.yview(MOVETO, 1.0)

                                 
    def send(self, widget):
        for data in self.entry.get().split('\n'):
            if data.startswith(self.DELIMITER):
                self.update_screen('>>> %s <<<\n' % data.strip(self.DELIMITER))
                trigged = self.trigger_event.matchall(data)
                trigged = list(trigged)
                print(trigged)
                if trigged:
                    for event, group in trigged:
                        self.module.signal(event, group, self.server, self.view, self)
                else:
                    self.server.send_cmd('%s', data.strip(self.DELIMITER))
            else:
                for line in ircwrap.wrap(data):
                    self.update_screen('<%s>%s\n' % (self.server.nick, line))
                    self.server.send_cmd('PRIVMSG %s :%s', (self.target, line))
                   
        self.entry.delete(0, END)

    def redisplay(self):
        self.withdraw()
        
        self.update()
        self.deiconify()

# It has to be defined here. A call to Module constructor imports
# all plugins at once. Some of them plugin might very well import
# user module consequently if it is set when the class is being constructed
# it will throw an exception cause the class User isnt constructed at the time
# it was imported.

import os
PATH = os.path.join(os.path.dirname(__file__), 'userevent.txt')

User.trigger_event = Trigger(PATH)
User.module = Module('nerdlib.usermod')

if __name__ == '__main__':
    user = User()
    user.mainloop()











