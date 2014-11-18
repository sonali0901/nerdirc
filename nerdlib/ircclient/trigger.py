import re
import json

class Trigger:
    def __init__(self, module):
        self.module = module

        with open(module, 'r') as f:
            data = f.read()

        rgx = json.loads(data)

        self.web = {}

        for i in rgx.keys():
            self.web[i] = re.compile(*rgx[i])
            
    def matchall(self, data):
        for i in self.web.keys():
            matched = self.web[i].match(data)
        
            if matched != None:
                yield((i, matched.groupdict()))
   

