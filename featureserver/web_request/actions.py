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
        ''' returns a list of contraint objects '''
        pass
    
    @property
    def sort(self):
        ''' returns a list of sort objects '''
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



class Insert(Action):
    def __init__(self, datasource, **kwargs):
        super(Insert, self).__init__("insert", datasource, **kwargs)

class Select(Action):
    def __init__(self, datasource, **kwargs):
        super(Select, self).__init__("select", datasource, **kwargs)

class Update(Action):
    def __init__(self, datasource, **kwargs):
        super(Update, self).__init__("update", datasource, **kwargs)

class Delete(Action):
    def __init__(self, datasource, **kwargs):
        super(Delete, self).__init__("delete", datasource, **kwargs)

