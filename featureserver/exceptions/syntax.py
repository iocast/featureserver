from .core import BaseException

class SyntaxException(BaseException):
    
    message="'%s' raised exception."
    
    def __init__(self, locator, layer="", code="", message="", dump = ""):
        self.message = self.message % locator
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)



class ServiceNotFoundException(BaseException):
    
    servcie = ""
    message="Service '%s' could not be found."
    
    def __init__(self, locator, service, layer="", code="", message="", dump = ""):
        self.service = service
        self.message = self.message % self.service
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)



class NoLayerException(BaseException):
    
    message="No Layer is configured."
    
    def __init__(self, locator, layer="", code="", message="", dump = ""):
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)


class MissingParameterException(BaseException):
    
    parameter=""
    message="Required parameter '%s' is missing."
    
    def __init__(self, locator, parameter, layer="", code="", message="", dump = ""):
        self.parameter = parameter
        self.message = self.message % self.parameter
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)


class NoGeometryException(BaseException):
    
    message="Geometry could not be found."
    
    def __init__(self, locator, layer, code="", message="", dump = ""):
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)



class TransactionNotSupported(BaseException):
    
    message="Transaction is not supported by service %s"
    
    def __init__(self, locator, layer="", code="", message="", dump = ""):
        self.message = self.message % service
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)


class VersionNotSupportedException(BaseException):
    
    message="Requested version '%s' is not supported. Use one of the following: %s"
    
    def __init__(self, locator, version, supported_versions, layer="", code="", message="", dump = ""):
        self.message = self.message % (version, ", ".join(supported_versions))
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)
