'''
Created on Dec 10, 2011

@author: michel
'''
from FeatureServer.Parsers.Parser import Parser

class WFSParser(Parser):
    ''' parses WFS-T and WFS GetFeature operations '''
    
    def __init__(self, service):
        Parser.__init__(self, service)
        self.actions = []
    
    def parse(self): pass

    def get_actions(self):
        return self.actions




