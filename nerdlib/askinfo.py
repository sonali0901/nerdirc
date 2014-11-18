from tkinter import *
from tkinter import ttk
from nerdlib import config

class AskInfo(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.resizable(width=False, height=False)

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.transient(root)

        self.title('Server info')

        self.frame1 = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        self.l1 = ttk.Label(self.frame1, text='Address')
        self.l2 = ttk.Label(self.frame1, text='Real name')
        self.l3 = ttk.Label(self.frame1, text='Nick')
        self.l4 = ttk.Label(self.frame1, text='user_name')
        self.l5 = ttk.Label(self.frame1, text='Port')
        self.l6 = ttk.Label(self.frame1, text='Server name')
        self.l7 = ttk.Label(self.frame1, text='Charset')

        self.e1 = ttk.Entry(self.frame1) 
        self.e2 = ttk.Entry(self.frame1)
        self.e3 = ttk.Entry(self.frame1) 
        self.e4 = ttk.Entry(self.frame1)
        self.e5 = ttk.Entry(self.frame1)
        self.e6 = ttk.Entry(self.frame1)
        self.e7 = ttk.Entry(self.frame1)

        self.frame2 = ttk.Frame(self, relief=RAISED, padding=(6, 6), border=3)
        self.t1 = Text(self.frame2, width=15, height=5)


        self.e1.insert(0, config.server_info['server_address'])
        self.e2.insert(0, config.server_info['real_name'])
        self.e3.insert(0, config.server_info['nick'])
        self.e4.insert(0, config.server_info['user_name'])
        self.e5.insert(0, config.server_info['port'])
        self.e6.insert(0, config.server_info['server_name'])
        self.e7.insert(0, config.server_info['charset'])
        self.t1.insert('end', 'PRIVMSG nickserv :identify password\nJOIN #calculus\nJOIN #Math')

        self.l1.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.l2.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.l3.grid(row=2, column=0, padx=3, pady=3, sticky=W)
        self.l4.grid(row=3, column=0, padx=3, pady=3, sticky=W)
        self.l5.grid(row=4, column=0, padx=3, pady=3, sticky=W)
        self.l6.grid(row=5, column=0, padx=3, pady=3, sticky=W)
        self.l7.grid(row=6, column=0, padx=3, pady=3, sticky=W)

        self.e1.grid(row=0, column=1, padx=3, pady=3)
        self.e2.grid(row=1, column=1, padx=3, pady=3)
        self.e3.grid(row=2, column=1, padx=3, pady=3)
        self.e4.grid(row=3, column=1, padx=3, pady=3)
        self.e5.grid(row=4, column=1, padx=3, pady=3)
        self.e6.grid(row=5, column=1, padx=3, pady=3)
        self.e7.grid(row=6, column=1, padx=3, pady=3)

        self.t1.pack(side='top', expand=True, fill=BOTH)
        self.frame1.pack(side='top', expand=True, fill=BOTH)
        self.frame2.pack(side='top', expand=True, fill=BOTH)

        self.f = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        b1 = ttk.Button(self.f, text="Ok", command=self.ok)
        b1.pack(side='left', fill=BOTH, expand=True, padx=3,pady=3)

        b2 = ttk.Button(self.f, text="Cancel", command=self.cancel)
        b2.pack(side='left', fill=BOTH, expand=True, padx=3, pady=3)

        self.f.pack(side='top', expand=True, fill=BOTH)

        self.bind("<Escape>", lambda widget: self.cancel())

        root.wait_window(self)

    def ok(self):
        self.result = [
                        self.e1.get(),
                        self.e2.get(),
                        self.e3.get(),
                        self.e4.get(),
                        int(self.e5.get()),
                        self.e6.get(),                      
                        self.e7.get(), 
                        self.t1.get('1.0', 'end').split('\n') 
                      ]

        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

    def get_info(self):
        return self.result

if __name__ == '__frame1__':
    root = Tk()

    d = AskInfo(root)







