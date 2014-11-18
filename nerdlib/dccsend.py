from tkinter import *
from tkinter import ttk
import sys
from socket import *
from select import select
from tkinter.messagebox import showinfo

class DccSend(Toplevel):
    def __init__(self, nick, filename, port):
        Toplevel.__init__(self)
        self.resizable(width=False, height=False)

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.title(nick)
        self.filename = filename
        self.f1 = ttk.Frame(self, relief=RAISED, padding=(5, 5), border=3)

        self.l1 = ttk.Label(self.f1, text='File name:%s' %  filename)
        self.l1.pack(side='top')

        self.f2 = ttk.Frame(self, relief=RAISED, padding=(5, 5), border=3)

        self.l2 = ttk.Label(self.f2, text='Not connected')
        self.l2.pack(side='top')

        self.f1.pack(side='top', expand=True, fill=BOTH)

        self.f2.pack(side='top', expand=True, fill=BOTH)

        self.f3 = ttk.Frame(self, relief=RAISED, padding=(5, 5), border=3)

        self.b1 = ttk.Button(self.f3, text="Cancel", command=self.cancel)
        self.b1.pack(side='left', fill=BOTH, expand=True, padx=5,pady=5)

        self.f3.pack(side='top', expand=True, fill=BOTH)

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(('', int(port))) 
        self.server.listen(5)

        self.client = None
        self.BLOCK = 8024
        self.fd = None
        self.after(200, self.handle_accept)
        

    def handle_accept(self):
        r, w, x = select([self.server], [], [], 0)
        if r:
            self.client, addr = self.server.accept()
            self.fd = open(self.filename, 'rb')
            self.server.close()
            self.after(200, self.handle_read_write)
            return
        self.after(200, self.handle_accept)

    def handle_read_write(self):
        r, w, x = select([self.client], [self.client], [], 0)
        if r:
            data = self.client.recv(8024)
            if not data:
                self.b1.config(text='Done')
                return 
        ################################
        if w:
            data = self.fd.read(self.BLOCK)
            self.client.sendall(data)
    ################################
            if not data:
                self.b1.config(text='Done')
                return
            self.l2.config(text='Pos:%s' % self.fd.tell())    
        #################################
        self.after(200, self.handle_read_write)

    def cancel(self):
        try:
            self.fd.close()
        except:
            pass

        try:
            self.client.close()
        except:
            pass
        
        try:
            self.server.close()
        except:
            pass

        self.destroy()


def ip_to_long (ip):
    """
    Convert ip address to a network byte order 32-bit integer.
   """
    quad = ip.split('.')
    if len(quad) == 1:
        quad = quad + [0, 0, 0]
    elif len(quad) < 4:
        host = quad[-1:]
        quad = quad[:-1] + [0,] * (4 - len(quad)) + host

    lip = 0
    for q in quad:
        lip = (lip << 8) | int(q)
    return lip


def long_to_ip (l):
    """
    Convert 32-bit integerto to a ip address.
    """
    return '%d.%d.%d.%d' % (l>>24 & 255, l>>16 & 255, l>>8 & 255, l & 255) 

if __name__ == '__main__':
    d = DccSend(sys.argv[1], sys.argv[2], sys.argv[3])
    d.mainloop()



