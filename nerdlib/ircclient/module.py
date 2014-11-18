import sys
from traceback import print_exc as debug

class Module:
    """ This class is used to load/unload plugins.
        It calls functions which are defined inside the plugin files
        according to their names. These name functions correspond to irc
        event commands. 
    """

    def __init__(self, *args1, **args2):
        self.modules = []

        for i in args1:
            self.load(i)

        for i, j in args2.items():
            self.load(i, **j)


    def load(self, module, **args):
        """ Load a plugin 
            once the plugin is loaded
            and changes are done in the plugin
            if it is loaded again the old plugin
            will keep in memory. it would need to be
            first unloaded to then load again with the
            new changes.
        """
        __import__(module)

        plugin = sys.modules[module]

        self.modules.append(plugin)

        if len(args):
            for i, j in args.items():
                setattr(plugin, i, j)
   
    
    def unload(self, module):
        """ Unload a plugin """
        plugin = sys.modules[module]
        self.modules.remove(plugin)
        del sys.modules[module]


    """ It sends a signal to a specific module """
    def signal_module(self, module, sign, *args1, **args2):
        if hasattr(module, sign):
            act = getattr(module, sign)
            """verify whether act receives argument or not """
            try:
                act(*args1, **args2)
            except Exception as exc:
                debug()
    """ It sends a signal to all modules """
    def signal(self, sign, *args1, **args2):
        for i in self.modules:
            self.signal_module(i, sign, *args1, **args2)


