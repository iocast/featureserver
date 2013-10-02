
from vectorformats.exceptions import BaseException


class ServiceException(BaseException):
    message="Service '%s' does not exists"
    
    def __init__(self, locator, service, layer="", code="", dump=""):
        if len(service) > 0:
            self.message = self.message % service
        BaseException.__init__(self, self.message, code, locator, service, layer, dump)

