'''
Created on Apr 20, 2011

@author: michel
'''
import os
from lxml import etree
from FeatureServer.Parsers.WebFeatureService.FilterEncoding.Operator import Operator

class LogicalOperator(Operator):
    def __init__(self, node):
        super(LogicalOperator, self).__init__(node)
        self.type = 'LogicalOperator'
        
    def createStatement(self, datasource, operatorList):
        logical = self.addOperators(operatorList)
                
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../../resources/filterencoding/logical_operators_%s.xsl" % datasource.type)
        transform = etree.XSLT(xslt)
        result = transform(logical, operationType="'"+str(self.node.xpath('local-name()'))+"'")
        elements = result.xpath("//Statement")
        if len(elements) > 0:
            self.setStatement(str(elements[0].text).strip())
            return
        self.setStatement(None)
        
    def addOperators(self, operatorList):
        logical = etree.Element(self.node.tag)
        
        for operator in operatorList:
            element = etree.Element("Operator")
            element.text = operator.stmt
            logical.append(element)
        
        return logical
    