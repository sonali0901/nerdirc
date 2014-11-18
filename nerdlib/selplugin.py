from tkinter import *
from tkinter import ttk
from nerdlib.askinfo import *
from nerdlib.askstring import *
import shelve
import os
from nerdlib.config import initialize

class SelectPlugin(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.root = root
        self.resizable(width=False, height=False)

        self.transient(root)

        self.title('Select plugin')

        self.main = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        self.listbox = Listbox(self.main)
        

        filename = initialize()
        self.config = shelve.open(filename, writeback=True)

        plugins = self.config['plugins']

        for ind in plugins:
            self.listbox.insert('end', ind)

        self.main.pack(side='top', expand=True, fill=BOTH)
        self.listbox.pack(side='top', expand=True, fill=BOTH)

        self.f = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        b1 = ttk.Button(self.f, text="Ok", command=self.ok)
        b1.pack(side='left', fill=BOTH, expand=True, padx=3,pady=3)

        b2 = ttk.Button(self.f, text="Add", command=self.add)
        b2.pack(side='left', fill=BOTH, expand=True, padx=3,pady=3)

        b3 = ttk.Button(self.f, text="Remove", command=self.remove)
        b3.pack(side='left', fill=BOTH, expand=True, padx=3,pady=3)

        self.f.pack(side='top', expand=True, fill=BOTH)
        self.bind("<Return>", lambda widget: self.ok())

        root.wait_window(self)

    def ok(self):
        self.config.close()
        self.destroy()

    def remove(self):
        sel = self.listbox.curselection()[0]
        sel = int(sel)
        del self.config['plugins'][sel]
        self.listbox.delete(sel)

    def add(self):
        askstring = AskString(self.root, 'Load plugin', 'Plugin')

        if not askstring.result:
            return

        self.config['plugins'].append(askstring.result)
        self.listbox.insert('end', askstring.result)

    def get_info(self):
        return self.result

if __name__ == '__main__':
    root = Tk()

    d = SelectPlugin(root)










