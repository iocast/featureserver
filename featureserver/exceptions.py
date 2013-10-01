
class ExceptionReport(object):
    index = 0
    exceptions = []
    
    def add(self, exception):
        self.exceptions.append(exception)
    
    def __len__(self):
        return len(self.exceptions)
    
    def __iter__(self):
        self.index = 0
        return self
    
    def next(self):
        if self.index >= len(self):
            raise StopIteration
        exception = self.exceptions[self.index]
        self.index += 1
        return exception
    
    def get(self, index):
        return self.exceptions[index]



class BaseException(Exception):
    @property
    def dump(self):
        return self._dump if self._dump else ""
    @property
    def code(self):
        return self._code if self._code else ""
    @property
    def locator(self):
        return self._locator if self._locator else ""
    @property
    def service(self):
        return self._service if self._service else ""
    @property
    def layer(self):
        return self._layer if self._layer else ""
    
    def __init__(self, message, code, locator, service, layer, dump):
        Exception.__init__(self, message)
        self._code = code
        self._locator = locator
        self._service = service
        self._layer = layer
        self._dump = dump



class ServiceException(BaseException):
    message="Service '%s' does not exists"
    
    def __init__(self, locator, service, layer="", code="", dump=""):
        if len(service) > 0:
            self.message = self.message % service
        BaseException.__init__(self, self.message, code, locator, service, layer, dump)

