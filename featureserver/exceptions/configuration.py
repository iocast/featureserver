
'''
    Created on October 15, 2012
    
    @author: michel
    '''

from .core import BaseException



class LayerNotFoundException(BaseException):
    
    message="Could not find the layer '%s': Check your config file for the missing layer. (Available layers are: %s)."
    
    def __init__(self, locator, layer, supported_layers, code="", message="", dump=""):
        self.message = self.message % (layer, ", ".join(supported_layers))
        if len(message) > 0:
            self.message = message
        BaseException.__init__(self, self.message, code, locator, layer, dump)
