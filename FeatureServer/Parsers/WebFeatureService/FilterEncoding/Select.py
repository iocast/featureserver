'''
Created on Dec 10, 2011

@author: michel
'''
from FilterEncoding import FilterEncoding
from WebRequest.Actions.Select import Select as SelectRequest

class Select(SelectRequest):
    ''' implements the interface of the a select action (guide through all the request from WebRequest.Actions.Select'''
    filter      = None
    properties  = []

    def __init__(self, datasource, data, properties = []):
        ''' data represents a <ogc:Filter/> '''
        SelectRequest.__init__(self, datasource=datasource)
        self.data   = data
        self.filter = FilterEncoding(data)
        self.properties = properties
        
        self.filter.parse();
    
    def get_statement(self):
        return self.filter.render(self.datasource)

    def get_attributes(self):
        return self.properties
        #return self.filter.getAttributes()
        
        