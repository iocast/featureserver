

class DataSource (object):
    """Base datasource class. Datasources override the insert, update,
        and delete methods to support those actions, and can optionally
        use begin, commit, and rollback methods to perform locking."""
    
    _query_actions = {}
    
    def __init__(self, name, **kwargs):
        self.name = name
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    def execute (self, action):
        raise NotImplementedError
    def insert (self, action):
        ''' returns a ActionResult '''
        raise NotImplementedError
    def update (self, action):
        ''' returns a ActionResult '''
        raise NotImplementedError
    def delete (self, action):
        ''' returns a ActionResult '''
        raise NotImplementedError
    def select (self, action):
        ''' returns a list of Feature '''
        pass
    
    def begin (self): pass
    def commit (self, close=True): pass
    def rollback (self, close=True): pass
    def close (self): pass
    
    def getBBOX(self):
        return '0 0 0 0'

    def getAttributes(self): pass

    def getFormatedAttributName(self, name):
        return name
    
    def getGeometry(self): pass
    def getAttributeDescription(self, attribute):
        ''' Returns a description of an attribute. Return format is (type, length) of the attribute. '''
        return ('string', '')

    def render(self, action):
        ''' Returns a data source specific statement based on the action object. E.g. a SQL statement for SpatialLite. '''
        pass

    @property
    def query_actions(self):
        return self._query_actions


