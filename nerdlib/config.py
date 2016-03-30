import shelve

server_info = {
                'server_address' :'irc.freenode.com', 
                'nick' : 'Tau', 
                'real_name' : 'Tente outra vez.', 
                'user_name' : 'Euler', 
                'port' : 6667,
                'server_name' : 'freenode',
                'charset' : 'utf-8'
              }

user_plugins = ['nerdlib.usermod']

def create_config_file(filename):
    data = shelve.open(filename, writeback=True)
    data['server_list'] = [
                                            (
                                            'irc.freenode.com',
                                            'Tente outra vez.',
                                            'Tau',
                                            'euler',
                                            6667,
                                            'Freenode',
                                            'utf-8',
                                            ['##calculus', '#vy']
                                            )
                          ]
    
    data['plugins'] = ['nerdlib.stdmod', 
           	           'nerdlib.startup',
                       'nerdlib.plugins.gossip.gossip', 
                       'nerdlib.plugins.nickcall.nickcall', 
                       'nerdlib.plugins.latex.latex',
           	           'nerdlib.plugins.highligh.highligh',
                       'nerdlib.plugins.link.link',
                       'nerdlib.plugins.ajoin.ajoin',
                       'nerdlib.plugins.nickclick.nickclick']
    
    data['text_theme'] = {
                            'background': '#fff1e8',
                            'foreground': 'black',
                            'font': ('Monospace', 9, 'bold'),
                         }
    
    
    data['entry_theme'] = {
                            'background': '#fff1e8',
                            'foreground': 'black',
                            'font': ('Monospace', 9, 'bold'),
                         }
    
    
    data['box_theme'] = {
                            'background': '#fff1e8',
                            'foreground': 'black',
                            'font': ('Monospace', 9, 'bold'),
                         }
    data.close()
    

def initialize():
    from os.path import expanduser, join, exists
    filename  = join(expanduser('~'), '.nerd.db')

    if not exists(filename):
        create_config_file(join(expanduser('~'), '.nerd.db'))

    return join(expanduser('~'), '.nerd.db')






