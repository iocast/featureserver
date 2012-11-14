'''
Created on Apr 5, 2011

@author: michel
'''

from ComparisonOperator import ComparisonOperator

class PropertyIsNull(ComparisonOperator):
    ''' '''
    def getPropertyName(self): return str(self.node.PropertyName)
        