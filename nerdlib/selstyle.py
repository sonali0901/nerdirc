from tkinter import *
from tkinter import ttk
from nerdlib import config
import os
import shelve
from nerdlib.config import initialize

class SelectStyle(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.resizable(width=False, height=False)

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.transient(root)

        self.title('Window style')
        filename = initialize()
        self.config = shelve.open(filename)


        self.main = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        self.l1 = ttk.Label(self.main, text='Text Background')
        self.l2 = ttk.Label(self.main, text='Text Foreground')
        self.l3 = ttk.Label(self.main, text='Text Font type')
        self.l4 = ttk.Label(self.main, text='Text Font size')
        self.l5 = ttk.Label(self.main, text='Text Font option')

        self.l6 = ttk.Label(self.main, text='Entry Background')
        self.l7 = ttk.Label(self.main, text='Entry Foreground')
        self.l8 = ttk.Label(self.main, text='Entry Font type')
        self.l9 = ttk.Label(self.main, text='Entry Font size')
        self.l10 = ttk.Label(self.main, text='Entry Font option')

        self.l11 = ttk.Label(self.main, text='Box Background')
        self.l12 = ttk.Label(self.main, text='Box Foreground')
        self.l13 = ttk.Label(self.main, text='Box Font type')
        self.l14 = ttk.Label(self.main, text='Box Font size')
        self.l15 = ttk.Label(self.main, text='Box Font option')

        self.e1 = ttk.Entry(self.main) 
        self.e2 = ttk.Entry(self.main)
        self.e3 = ttk.Entry(self.main) 
        self.e4 = ttk.Entry(self.main)
        self.e5 = ttk.Entry(self.main)

        self.e6 = ttk.Entry(self.main) 
        self.e7 = ttk.Entry(self.main)
        self.e8 = ttk.Entry(self.main) 
        self.e9 = ttk.Entry(self.main)
        self.e10 = ttk.Entry(self.main)
        self.e11 = ttk.Entry(self.main) 
        self.e12 = ttk.Entry(self.main)
        self.e13 = ttk.Entry(self.main) 
        self.e14 = ttk.Entry(self.main)
        self.e15 = ttk.Entry(self.main)


        self.e1.insert(0, self.config['text_theme']['background'])
        self.e2.insert(0, self.config['text_theme']['foreground'])
        font = self.config['text_theme']['font']
        self.e3.insert(0, font[0])
        self.e4.insert(0, font[1])
        self.e5.insert(0, font[2])

        self.e6.insert(0, self.config['entry_theme']['background'])
        self.e7.insert(0, self.config['entry_theme']['foreground'])
        font = self.config['entry_theme']['font']
        self.e8.insert(0, font[0])
        self.e9.insert(0,  font[1])
        self.e10.insert(0, font[2])

        self.e11.insert(0, self.config['box_theme']['background'])
        self.e12.insert(0, self.config['box_theme']['foreground'])
        font = self.config['box_theme']['font']
        self.e13.insert(0, font[0])
        self.e14.insert(0,  font[1])
        self.e15.insert(0, font[2])

        self.l1.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.l2.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.l3.grid(row=2, column=0, padx=3, pady=3, sticky=W)
        self.l4.grid(row=3, column=0, padx=3, pady=3, sticky=W)
        self.l5.grid(row=4, column=0, padx=3, pady=3, sticky=W)


        self.l6.grid(row=5, column=0, padx=3, pady=3, sticky=W)
        self.l7.grid(row=6, column=0, padx=3, pady=3, sticky=W)
        self.l8.grid(row=7, column=0, padx=3, pady=3, sticky=W)
        self.l9.grid(row=8, column=0, padx=3, pady=3, sticky=W)
        self.l10.grid(row=9, column=0, padx=3, pady=3, sticky=W)

        self.l11.grid(row=10, column=0, padx=3, pady=3, sticky=W)
        self.l12.grid(row=11, column=0, padx=3, pady=3, sticky=W)
        self.l13.grid(row=12, column=0, padx=3, pady=3, sticky=W)
        self.l14.grid(row=13, column=0, padx=3, pady=3, sticky=W)
        self.l15.grid(row=14, column=0, padx=3, pady=3, sticky=W)

        self.e1.grid(row=0, column=1, padx=3, pady=3)
        self.e2.grid(row=1, column=1, padx=3, pady=3)
        self.e3.grid(row=2, column=1, padx=3, pady=3)
        self.e4.grid(row=3, column=1, padx=3, pady=3)
        self.e5.grid(row=4, column=1, padx=3, pady=3)

        self.e6.grid(row=5, column=1, padx=3, pady=3)
        self.e7.grid(row=6, column=1, padx=3, pady=3)
        self.e8.grid(row=7, column=1, padx=3, pady=3)
        self.e9.grid(row=8, column=1, padx=3, pady=3)
        self.e10.grid(row=9, column=1, padx=3, pady=3)

        self.e11.grid(row=10, column=1, padx=3, pady=3)
        self.e12.grid(row=11, column=1, padx=3, pady=3)
        self.e13.grid(row=12, column=1, padx=3, pady=3)
        self.e14.grid(row=13, column=1, padx=3, pady=3)

        self.e15.grid(row=14, column=1, padx=3, pady=3)
        self.main.pack(side='top', expand=True, fill=BOTH)

        self.f = ttk.Frame(self, relief=RAISED, padding=(3, 3), border=3)

        b1 = ttk.Button(self.f, text="Ok", command=self.ok)
        b1.pack(side='left', fill=BOTH, expand=True, padx=3,pady=3)

        b2 = ttk.Button(self.f, text="Cancel", command=self.cancel)
        b2.pack(side='left', fill=BOTH, expand=True, padx=3, pady=3)

        self.f.pack(side='top', expand=True, fill=BOTH)

        self.bind("<Return>", lambda widget: self.ok())
        self.bind("<Escape>", lambda widget: self.cancel())


        root.wait_window(self)

    def ok(self):
        self.config['text_theme'] = {
                                      'background': self.e1.get(),
                                      'foreground': self.e2.get(),
                                      'font': (self.e3.get(), int(self.e4.get()), self.e5.get())
    			            }

        self.config['entry_theme'] = {
                                      'background': self.e6.get(),
                                      'foreground': self.e7.get(),
                                      'font': (self.e8.get(), int(self.e9.get()), self.e10.get())
    			            }

        self.config['box_theme'] = {
                                      'background': self.e11.get(),
                                      'foreground': self.e12.get(),
                                      'font': (self.e13.get(), int(self.e14.get()), self.e15.get())
    			            }

        self.config.close()
        self.destroy()

    def cancel(self):
        self.destroy()

if __name__ == '__main__':
    root = Tk()
    d = SelectStyle(root)








