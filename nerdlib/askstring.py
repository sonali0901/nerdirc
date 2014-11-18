from tkinter import *
from tkinter import ttk

class AskString(Toplevel):
    def __init__(self, root, title, question):
        Toplevel.__init__(self, root)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.transient(root)

        self.title(title)

        ttk.Label(self, text=question).pack()

        self.e = ttk.Entry(self)
        self.e.pack(padx=5)

        self.e.focus_set()

        self.f = Frame(self)
        b1 = ttk.Button(self.f, text="Ok", command=self.ok)
        b1.pack(side='left', pady=5)

        b2 = ttk.Button(self.f, text="Cancel", command=self.cancel)
        b2.pack(side='left', pady=5)

        self.f.pack(side='top')

        self.bind("<Return>", lambda widget: self.ok())
        self.bind("<Escape>", lambda widget: self.cancel())

        root.wait_window(self)

    def ok(self):
        self.result = self.e.get()
        self.destroy()

    def cancel(self):
        self.result = ''
        self.destroy()

if __name__ == '__main__':
    root = Tk()
    d = MyDialog(root, 'hi', 'haha')
    print(d.result)
