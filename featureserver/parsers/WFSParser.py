'''
Created on Dec 10, 2011

@author: michel
'''
from Parser import Parser
from featureserver.web_request.operators import Constraint, Sort


class WFSParser(Parser):
    ''' parses WFS-T and WFS GetFeature operations '''
    
    def __init__(self, service):
        Parser.__init__(self, service)
    
    def parse(self): pass
    
    def add_action(self, action):
        self.service.datasources[action.datasource.name].append(action)
    def add_actions(self, actions):
        for action in actions:
            self.service.datasources[action.datasource.name].append(action)



    def parse_sort(self):
        sort = []
        
        if "sort" in self.service.request.params:
            sort_list = self.service.request.params['sortby'].split(",")
            for item in sort_list:
                attribute, operator = item.split("_")
                sort.append(Sort(attribute=attribute, operator=operator))
        
        return sort
    
    def parse_constraints(self):
        constraints = []
        
        if "queryable" in self.service.request.params:
            query_list = self.service.request.params['queryable'].split(",")
            
            for key, value in self.service.request.params.iteritems():
                if "__" in key:
                    attribute, operator = key.split("__")
                    if attribute in query_list:
                        constraints.append(Constraint(attribute=attribute, value=self.service.request.params[key], operator=operator))
        
        return constraints



