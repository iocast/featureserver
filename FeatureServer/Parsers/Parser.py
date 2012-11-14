

class Parser(object):
    
    def __init__(self, request):
        self._request = request
    
    @property
    def request(self):
        return self._request
    
    def parse(self): pass
    def get_actions(self): pass

