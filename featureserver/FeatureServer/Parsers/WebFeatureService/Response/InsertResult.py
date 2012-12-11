'''
'''

from ActionResult import ActionResult

class InsertResult(ActionResult):
    
    def __init__(self, handle):
        ActionResult.__init__(self, handle)
        self.type = 'insert'
