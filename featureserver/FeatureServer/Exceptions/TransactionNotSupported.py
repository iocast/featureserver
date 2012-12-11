'''
Created on November 11, 2012
    
@author: michel
'''

from FeatureServer.Exceptions.BaseException import BaseException

class TransactionNotSupported(BaseException):
    
    message="Transaction is not supported by service %s"
    
    def __init__(self, locator, layer="", code="", message="", dump = ""):
        self.message = self.message % service
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)