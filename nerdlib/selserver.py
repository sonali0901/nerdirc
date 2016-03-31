from tkinter import *
from tkinter import ttk
from nerdlib.askinfo import *
import shelve
import os
from nerdlib.config import initialize

class SelectServer(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.root = root
        self.resizable(width=False, height=False)

        self.transient(root)

        self.title('Select server')

        self.frame1 = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        self.listbox = Listbox(self.frame1)


        filename = initialize()
        self.config = shelve.open(filename, writeback=True)

        server_list = self.config['server_list']

        for ind in server_list:
            self.listbox.insert('end', ind[5])

        self.frame1.pack(side='top', expand=True, fill=BOTH)
        self.listbox.pack(side='top', expand=True, fill=BOTH)

        self.f = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        b1 = ttk.Button(self.f, text="Ok", command=self.ok)
        b1.pack(side='left', fill=BOTH, expand=True, padx=3, pady=3)

        b2 = ttk.Button(self.f, text="Cancel", command=self.cancel)
        b2.pack(side='left', fill=BOTH, expand=True, padx=3, pady=3)

        b3 = ttk.Button(self.f, text="Add", command=self.add)
        b3.pack(side='left', fill=BOTH, expand=True, padx=3,pady=3)

        b4 = ttk.Button(self.f, text="Remove", command=self.remove)
        b4.pack(side='left', fill=BOTH, expand=True, padx=3,pady=3)

        self.f.pack(side='top', expand=True, fill=BOTH)
        self.bind("<Return>", lambda widget: self.ok())
        self.bind("<Escape>", lambda widget: self.cancel())
        self.config.close()

        root.wait_window(self)

    def ok(self):
        filename = initialize()
        self.config = shelve.open(filename, writeback=True)

        sel = self.listbox.curselection()[0]
        sel = int(sel)
        self.result = self.config['server_list'][sel]
        self.config.close()
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

    def remove(self):
        filename = initialize()
        self.config = shelve.open(filename, writeback=True)

        sel = self.listbox.curselection()[0]
        sel = int(sel)
        del self.config['server_list'][sel]
        self.listbox.delete(sel)
        self.config.close()

    def add(self):
        askinfo = AskInfo(self.root)
        filename = initialize()
        self.config = shelve.open(filename, writeback=True)

        self.config['server_list'].append(askinfo.result)
        self.listbox.insert('end', askinfo.result[5])
        self.config.close()

    def get_info(self):
        return self.result

if __name__ == '__frame1__':
    root = Tk()

    d = SelectServer(root)











