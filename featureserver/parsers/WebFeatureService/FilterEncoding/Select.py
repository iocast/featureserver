'''
Created on Dec 10, 2011

@author: michel
'''
from FilterEncoding import FilterEncoding
from featureserver.web_request.actions import Select as SelectRequest

class Select(SelectRequest):
    ''' implements the interface of the a select action (guide through all the request from FeatureServer.WebRequest.Actions.Select'''

    def __init__(self, datasource, data, service, ids = [], attributes = [], constraints = [], sort = [], **kwargs):
        ''' data represents a <ogc:Filter/> '''
        super(Select, self).__init__(datasource=datasource, **kwargs)
        self.type           = "select"
        self._stmt          = None
        
        self._data          = data
        self._service       = service
        self._ids           = ids
        self._attributes    = attributes
        self._constraints   = constraints
        self._sort          = sort
        
        self._filter        = FilterEncoding(xml = self._data) if self._data is not None else None
        
        if self.filter is not None:
            self.filter.parse()
            self._stmt = self.filter.render(datasource = self.datasource, service = self.service)
    
    
    # override
    @property
    def statement(self):
        return self._stmt
    @property
    def ids(self):
        return self._ids
    @property
    def attributes(self):
        return self._attributes
    @property
    def constraints(self):
        return self._constraints
    @property
    def sort(self):
        return self._sort
    # end

    
    @property
    def filter(self):
        return self._filter
    @property
    def service(self):
        return self._service