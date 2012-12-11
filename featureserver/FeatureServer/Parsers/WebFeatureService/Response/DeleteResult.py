'''
'''

from ActionResult import ActionResult

class DeleteResult(ActionResult):
    
    def __init__(self, handle):
        ActionResult.__init__(self, handle)
        self.type = 'delete'
