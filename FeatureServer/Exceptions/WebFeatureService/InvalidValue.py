'''
Created on May 24, 2011

@author: michel
'''
from FeatureServer.Exceptions.WFSException import WFSException

class InvalidValue(WFSException):
    def __init__(self, **kwargs):
        super(InvalidValue, self).__init__(**kwargs)
        self.code = 'InvalidParameterValue'
        self.message = 'ValueReference does not exist.'

    def getXML(self):
        return "<Exception exceptionCode=\"%s\" locator=\"%s\"><ExceptionText>%s</ExceptionText><ExceptionDump>%s</ExceptionDump></Exception>" % (self.code, self.locator, self.message, self.dump)
        