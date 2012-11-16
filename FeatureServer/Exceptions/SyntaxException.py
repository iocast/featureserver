from FeatureServer.Exceptions.BaseException import BaseException

class SyntaxException(BaseException):
    
    message="'%s' raised exception."
    
    def __init__(self, locator, layer="", code="", message="", dump = ""):
        self.message = self.message % self.locator
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)