'''
Created on May 24, 2011
    
@author: michel
'''

from .core import BaseException

class WFSException(BaseException):
    def __init__(self, locator, layer, message, code="", dump = ""):
        BaseException.__init__(self, message, code, locator, layer, dump)


class InvalidValueException(WFSException):
    def __init__(self, **kwargs):
        super(InvalidValueException, self).__init__(code="InvalidParameterValue", message="ValueReference does not exist.", **kwargs)
