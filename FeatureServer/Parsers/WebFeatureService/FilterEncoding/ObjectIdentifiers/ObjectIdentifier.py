'''
Created on Apr 20, 2011

@author: michel
'''
import os
from lxml import etree
from FeatureServer.Parsers.WebFeatureService.FilterEncoding.Operator import Operator

class ObjectIdentifier(Operator):
    def __init__(self, node):
        super(ObjectIdentifier, self).__init__(node)
        self.type = 'ObjectIndentifier'
    
    def getResourceId(self): return str(self.node.attrib('rid'))
    def createStatement(self, datasource, service):
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../../resources/filterencoding/object_identifiers_%s.xsl" % datasource.type)
        transform = etree.XSLT(xslt)
        result = transform(self.node, attributeIdName="'"+datasource.fid_col+"'")
        elements = result.xpath("//Statement")
        if len(elements) > 0:
            self.setStatement(str(elements[0]))
            return
        self.setStatement(None)
                