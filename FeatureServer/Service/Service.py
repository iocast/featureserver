
class Service (object):
    
    query_action_types = []
    
    def __init__ (self, request):
        self._request     = request
    
    @property
    def request(self):
        return self._request
    
    def encode(self): pass
    def get_capabilities(self): pass
    def describe_feature_type(self): pass
