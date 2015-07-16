from tkinter import *
from tkinter import ttk
from nerdlib.user import *
from nerdlib.config import initialize

class Channel(User):
    #DELIMITER = ':'

    def __init__(self, 
                 server=None, 
                 target=None,
                 view=None,
                 *args, 
                 **kwargs):

        Toplevel.__init__(self,  *args, **kwargs)

        self.server = server
        self.target = target
        self.view = view
        self.title(target)

        self.menubar = Menu(master=self)

        self.chanmenu = Menu(self.menubar, tearoff = 0) 
   
        self.chanmenu.add_command(label='Save buffer', command=self.save_buffer)
        self.chanmenu.add_separator()
        self.chanmenu.add_command(label='Close', command = self.withdraw)

        self.menubar.add_cascade(label='Channel', menu=self.chanmenu)

        self.config(menu=self.menubar)

 
        self.left = ttk.Frame(self,
                              relief = RAISED,
                              padding=(3, 3),
                              border=3)

        self.scrollbox = ttk.Scrollbar(master=self.left)

        filename = initialize()
        self.config = shelve.open(filename, writeback=True)


        box_theme = self.config['box_theme']

        self.box = Listbox(master=self.left, 
                           yscrollcommand=self.scrollbox.set,
                           **box_theme)

        self.box.bind('<Double-Button-1>', self.open_pvt) 

        self.scrollbox.config(command=self.box.yview)
        self.scrollbox.pack(side='right', fill=Y)



        self.left.pack(side='left', fill=Y)

        self.right = Frame(self)


        self.top = ttk.Frame(self.right,
                             relief = RAISED,
                             padding=(3, 3), 
                             border=3)


        self.scrollbar = ttk.Scrollbar(master=self.top)

 
        text_theme = self.config['text_theme']
        self.text = Text(master=self.top, 
                         yscrollcommand=self.scrollbar.set,
                         **text_theme)

        
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(side='right', fill=Y)


        
        self.down = ttk.Frame(self.right,
                              relief = RAISED,
                              padding=(3, 3), 
                              border=3)

        entry_theme = self.config['entry_theme']

        self.entry = Entry(master=self.down,
                               **entry_theme)


        self.entry.pack(fill=X)        
        self.entry.focus_set()

        self.text.pack(side='left', expand=True, fill=BOTH)
        self.box.pack(expand=True, fill=Y)
        self.right.pack(side='right', expand=True, fill=BOTH)
        self.down.pack(side='bottom', fill=X)
        self.top.pack(side='top', expand=True, fill=BOTH)
        self.entry.bind('<KeyPress-Return>', self.send)


        self.popup = Menu(self.entry, tearoff = 0)

        self.popup.add_command(label="Copy")

        self.popup.add_command(label="Cut")

        self.popup.add_command(label="Paste")

        self.popup.add_command(label="Select all")

        self.entry.bind('<Button-3>', self.post_popup)

        self.text.bind('<Button-3>', self.post_popup)

        self.entry.bind('<KeyPress-Tab>', self.tab)

        self.protocol('WM_TAKE_FOCUS', self.entry.focus_set)
   
    def open_pvt(self, widget):
        ind = self.box.index(ACTIVE)
        nick = self.box.get(ind)

        if self.view.get_win((self.server.getName(), nick.lower())):
            return

        wuser = User(self.server, nick)

        self.view.add_win(wuser, 
                          self.server.getName(), 
                          'end', 
                          (self.server.getName(), nick.lower()), 
                          text=nick)

    def tab(self, widget):
        data = self.entry.get().lower()
        data = data.rsplit(' ', 1)

        try:
            left, right= data
            pos = len(left)
        except:
            right = data[0]
            pos = 0
         
        if not len(right):
            return 'break'

        group = self.box.get(0, END)

        for ind in group:
            if not ind.lower().startswith(right):
                continue

            self.entry.delete(pos, END)
            self.entry.insert(END, ' %s ' % ind)
            break
        return 'break'

    
if __name__=='__main__':
    app = Channel()
    app.mainloop()
    pass








