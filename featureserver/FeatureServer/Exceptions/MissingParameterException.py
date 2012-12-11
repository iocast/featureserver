'''
Created on October 10, 2012
    
@author: michel
'''

from FeatureServer.Exceptions.BaseException import BaseException

class MissingParameterException(BaseException):
    
    parameter=""
    message="Required parameter '%s' is missing."
    
    def __init__(self, locator, parameter, layer="", code="", message="", dump = ""):
        self.parameter = parameter
        self.message = self.message % self.parameter
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)
