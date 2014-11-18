
class Dispatcher(object):
    def __init__(self, hold, *args, **kwargs):
        self.hold = hold
        self.args = args
        self.kwargs = kwargs

    def dispatch(self):
        for ind in self.hold.obj[:]:
            if not ind.isAlive():
                self.hold.obj.remove(ind)

            while ind.queue.qsize():
                for event, group in ind.queue.get(0):
                    self.hold.signal(event, 
                                     group,
                                     ind, 
                                     *self.args, 
                                     **self.kwargs)

            #If the thread is dead then removes it.

