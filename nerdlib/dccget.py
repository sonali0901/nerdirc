from tkinter import *
from tkinter import ttk
import sys
from socket import *
from select import select
from tkinter.messagebox import showinfo
from nerdlib.dccsend import long_to_ip
from struct import pack

from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, ECONNRESET, EINVAL, \
ENOTCONN, ESHUTDOWN, EINTR, EISCONN, EBADF, ECONNABORTED, EPIPE, EAGAIN 
CLOSE_ERR_CODE = (ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED, EPIPE, EBADF)
ACCEPT_ERR_CODE  = (EWOULDBLOCK, ECONNABORTED, EAGAIN)

def sendall2(sock, data):
    data = memoryview(data)
    sent = 0
    while data:
        try:
            sent = sent + sock.send(data)
            data = data[sent:]
        except error as excpt:
            err = excpt.args[0]
            if err in CLOSE_ERR_CODE:
                raise

class DccGet(Toplevel):
    BLOCK = 8024
    def __init__(self, nick, ip, filename, filesize, port):
        try:
            self.client = socket(AF_INET, SOCK_STREAM)
            self.client.connect((long_to_ip(int(ip)), int(port)))
        except Exception as excpt:
            showinfo('Error', 'Impossible to connect.')
            raise

        try:
            self.fd = open(filename, 'wb')
        except IOError:
            showinfo('Error', 'Failed to create the file.')
            raise

        self.client.setblocking(0)

        Toplevel.__init__(self)
        self.resizable(width=False, height=False)

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.title(nick)
        self.filename = filename
        self.filesize = filesize

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

        self.after(1, self.reactor)
        
    def reactor(self):
        try:
            data = self.client.recv(8024)
        except error as excpt:
            err = excpt.args[0]

            # If it is the case of the connection being closed
            if err in CLOSE_ERR_CODE:
                self.set_status()
            else:
                self.after(1, self.reactor)
        else:
            if not data:
                self.set_status()
            else:
                self.fd.write(data)
                ack = pack('!I', self.fd.tell())
                try:
                    sendall2(self.client, ack)
                except error as excpt:
                    self.set_status()
                else:
                    status = 'Pos:%s' % self.fd.tell()
                    self.l2.config(text=status)    
                    self.after(1, self.reactor)

    def set_status(self):
        if self.fd.tell() >= self.filesize:
            self.b1.config(text='Done')
        else:
            self.b1.config(text='Failed')

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


if __name__ == '__main__':
    d = DccSend(sys.argv[1], sys.argv[2], sys.argv[3])
    d.mainloop()







