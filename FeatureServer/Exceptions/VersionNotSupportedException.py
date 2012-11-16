'''
    Created on October 15, 2012
    
    @author: michel
    '''

from FeatureServer.Exceptions.BaseException import BaseException

class VersionNotSupportedException(BaseException):
    
    message="Requested version '%s' is not supported: Use one of the following: %s"
    
    def __init__(self, locator, version, supported_versions, layer="", code="", message="", dump = ""):
        self.message = self.message % (version, ", ".join(supported_versions))
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)
