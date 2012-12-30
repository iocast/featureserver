'''
Created on October 15, 2012
    
@author: michel
'''


class BaseException(Exception):
    dump = ""
    code = ""
    locator = ""
    layer = ""
    
    def __init__(self, message, code, locator, layer, dump):
        Exception.__init__(self, message)
        self.code = code
        self.locator = locator
        self.layer = layer
        self.dump = dump



class ExceptionReport():
    
    def __init__(self):
        self.index = 0
        self.exceptions = []
    
    def add(self, exception):
        self.exceptions.append(exception)
    
    def extend(self, exceptions):
        self.exceptions.extend(exceptions)
    
    def has_exceptions(self):
        if len(self.exceptions) > 0:
            return True
        return False
    
    def __len__(self):
        return len(self.exceptions)
    
    def __iter__(self):
        self.index = 0
        return self
    
    def next(self):
        if self.index >= len(self):
            raise StopIteration
        exception = self.exceptions[self.index]
        self.index += 1
        return exception
    
    def get(self, index):
        return self.exceptions[index]



