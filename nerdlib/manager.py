from tkinter import *
from tkinter import ttk
from nerdlib.user import *

class Manager(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        ttk.Treeview.__init__(self, *args, **kwargs)
        self.bind('<Double-Button-1>', self.display) 
        self.obj = dict()

    def add_win(self, window, parent, index, iid=None, **kwargs):
        self.insert(parent, index, str(iid), **kwargs)
        self.obj[str(iid)] = window

        window.protocol('WM_DELETE_WINDOW', window.withdraw)
        window.bind('<KeyPress-Escape>', lambda widget: window.withdraw())

    def del_win(self, name):
        for ind in self.get_children(str(name)) + (str(name),) :
            self.obj[ind].destroy()
            del self.obj[ind]
            self.delete(ind)

    def get_win(self, name):
        ind = str(name)
        return self.obj.get(ind)

    def display(self, widget):
        # Since we are in single selection mode
        choice = self.selection()[0]
        self.obj[choice].update()
        self.obj[choice].deiconify()
        return 'break'


if __name__ == '__main__':
    root = Tk()
    manager = Manager(master=root)
    main = User(master=manager)
    alphaA = User(master=manager)
    alphaB = User(master=manager)
    manager.add_win(main, '', 'end', '1', text='Server #1')

    #manager.add_win(main, '1', 'end', 'irc.freenode.org', text='irc.freenode.org')
    manager.add_win(alphaA, '1', 'end', 'main alphaA', text='alphaA')
    manager.add_win(alphaB, '1', 'end', 'main alphaB', text='alphaB')

    manager.pack()
    root.mainloop()

