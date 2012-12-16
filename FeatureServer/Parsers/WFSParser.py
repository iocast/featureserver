'''
Created on Dec 10, 2011

@author: michel
'''
from FeatureServer.Parsers.Parser import Parser

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
