from nerdlib.ircclient.server import *
from nerdlib.ircclient.module import *

class Hold(Module):
    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.obj = []

    def new_server(self, *args, **kwargs):
        """ instantiates a server instance and returns
            its reference and its index order
        """
        server = Server(*args, **kwargs)
        server.connect()
        self.obj.append(server)
        return server

    def del_server(self, server):
        pass


