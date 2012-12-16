'''
Created on Dec 10, 2011

@author: michel
'''
from FilterEncoding import FilterEncoding
from FeatureServer.WebRequest.Actions.Select import Select as SelectRequest

class Select(SelectRequest):
    ''' implements the interface of the a select action (guide through all the request from FeatureServer.WebRequest.Actions.Select'''

    def __init__(self, datasource, data, service, properties = []):
        ''' data represents a <ogc:Filter/> '''
        SelectRequest.__init__(self, datasource=datasource)
        self.type       = "select"
        
        self.data       = data
        self.filter     = FilterEncoding(xml = data)
        self.service    = service
        self.properties = properties
        
        self.filter.parse();
    
    def get_statement(self):
        return self.filter.render(datasource = self.datasource, service = self.service)

    def get_attributes(self):
        return self.properties
        
        