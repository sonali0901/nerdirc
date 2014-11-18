import textwrap

def wrap(data):
    LENGTH = 512
    """ Wrap data to send through network. """

    for line in data.split('\n'):
        for chunk in textwrap.wrap(line, LENGTH):
            yield(chunk)        
