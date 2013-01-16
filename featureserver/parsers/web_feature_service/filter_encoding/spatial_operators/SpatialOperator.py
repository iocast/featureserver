'''
Created on Apr 5, 2011

@author: michel
'''
import os
from lxml import etree
from featureserver.parsers.web_feature_service.filter_encoding.operator import Operator

class SpatialOperator(Operator):
    def __init__(self, node):
        super(SpatialOperator, self).__init__(node)
        self.type = 'SpatialOperator'
    
    def getValueReference(self): return str(self.node.ValueReference)
    def getLiteral(self): return str(self.node.Literal)
    def createStatement(self, datasource, service):
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../assets/transformation/filterencoding/spatial_operators_%s.xsl" % datasource.type)
        transform = etree.XSLT(xslt_input=xslt)
        result = transform(self.node, geometryName="'"+datasource.geom_col+"'", srs="'"+str(datasource.srid)+"'")
        
        stmtTxt = ''
        stmtChild = ''
        
        elements = result.xpath("//Statement")
        if len(elements) > 0:
            stmtTxt = elements[0].text
            
            
            elements = result.xpath("//Statement/*")
            if len(elements) > 0:
                stmtChild = etree.tostring(elements[0])
            
            self.setStatement(stmtTxt + stmtChild)
            return
        self.setStatement(None)
    