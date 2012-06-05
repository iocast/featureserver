'''
Created on May 24, 2011

@author: michel
'''

class WFSException(object):
    locator = 'service'
    dump = ''
    code = ''
    message = ''
    
    def __init__(self, **kwargs):        
        for key, val in kwargs.iteritems():
            setattr(self, key, val)
    
    def getXML(self): pass