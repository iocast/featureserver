'''
'''

from ActionResult import ActionResult

class UpdateResult(ActionResult):
    
    def __init__(self, handle):
        ActionResult.__init__(self, handle)
        self.type = 'update'
        