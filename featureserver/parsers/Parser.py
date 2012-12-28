

class Parser(object):
    
    def __init__(self, service):
        self._service = service
    
    @property
    def service(self):
        return self._service
    @property
    def request(self):
        return self.service.request
    
    def parse(self): pass
    