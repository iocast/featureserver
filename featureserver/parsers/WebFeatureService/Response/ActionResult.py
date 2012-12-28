'''
Created on Oct 21, 2011

@author: michel
'''

class ActionResult(object):
    
    def __init__(self, handle):
        self._handle    = handle
        self._resources = []
        self._index     = 0
    
    @property
    def handle(self):
        return self._handle
    
    def add(self, resourceId):
        self._resources.append(resourceId)
    def extend(self, resources):
        self._resources.extend(resources)

    def __len__(self):
        return len(self._resources)

    def __iter__(self):
        self._index = 0
        return self

    def next(self):
        if self._index >= len(self):
            raise StopIteration
        id = self._resources[self._index]
        self._index += 1
        return id

    def get(self, index):
        return self._resources[index]
    
