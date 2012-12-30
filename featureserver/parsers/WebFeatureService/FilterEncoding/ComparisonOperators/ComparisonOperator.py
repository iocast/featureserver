'''
Created on Apr 5, 2011

@author: michel
'''
import os
from lxml import etree
from ..Operator import Operator

class ComparisonOperator(Operator):
    def __init__(self, node):
        super(ComparisonOperator, self).__init__(node)
        self.type = 'ComparisonOperator'
    
    def getValueReference(self): return str(self.node.ValueReference)
    def getPropertyName(self): return str(self.node.PropertyName)
    def getLiteral(self): return str(self.node.Literal)
    def createStatement(self, datasource, service):
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../assets/transformation/filterencoding/comparison_operators_%s.xsl" % datasource.type)
        transform = etree.XSLT(xslt)
        
        # TODO: data source need to get parameters as **kwargs
        if hasattr(datasource, 'hstore'):
            result = transform(self.node, hstoreAttribute="'" + str(datasource.hstore_attr) + "'")
        else:
            result = transform(self.node)

        elements = result.xpath("//Statement")
        if len(elements) > 0:
            self.setStatement(str(elements[0]))
            return
        self.setStatement(None)
    