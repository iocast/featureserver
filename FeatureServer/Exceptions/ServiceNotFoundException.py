

from FeatureServer.Exceptions.BaseException import BaseException

class ServiceNotFoundException(BaseException):
    
    servcie = ""
    message="Service '%s' not found"
    
    def __init__(self, locator, service, layer="", code="", message="", dump = ""):
        self.service = service
        self.message = self.message % self.service
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)