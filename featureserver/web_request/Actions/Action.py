'''
'''

class Action (object):
    def __init__ (self, method, datasource, **kwargs):
        super(Action, self).__init__(**kwargs)
        self._method         = method
        self._datasource     = datasource
    
    
    @property
    def statement(self):
        ''' returns a datasource specific statement. For example for datasources which supports SQL it is the where clause. '''
        pass
    
    @property
    def ids(self):
        ''' returns a list of feature's ids '''
        pass
    
    @property
    def attributes(self):
        ''' returns a unique list of attributes to be queried '''
        pass
    
    @property
    def constraints(self):
        ''' returns a dict of constraints
            the following format is required
            [
                <name>__<operator> : {
                    column : '<name>',
                    type   : '<operator>',
                    value  ' '<value>'
                },
                ...
            ]
        '''
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

