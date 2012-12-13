'''
'''

class Action (object):
    def __init__ (self, method, datasource, **kwargs):
        super(Action, self).__init__(**kwargs)
        self._method         = method
        self._datasource     = datasource
    
    
    def get_statement(self):
        ''' returns a statement. E.g. for SQL it is the where clause '''
        pass
    
    def get_attributes(self):
        ''' returns a list of attributes '''
        pass
    
    def get_ids(self):
        ''' returns a list of ids of features to be modified '''
        pass
    
    
    @property
    def method(self):
        return self._method
    @property
    def datasource(self):
        return self._datasource
    @property
    def layer(self):
        return self._datasource.name


