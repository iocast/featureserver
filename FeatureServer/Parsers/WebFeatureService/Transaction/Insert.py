'''
Created on Oct 16, 2011

@author: michel
'''
import os, re
from lxml import etree

from TransactionAction import TransactionAction
from WebRequest.Actions.Insert import Insert as InsertAction

class Insert(TransactionAction, InsertAction):
    
    def __init__(self, datasource, node):
        super(Insert, self).__init__(datasource=datasource, node=node)
        self.type = 'insert'
    
    def create_statement(self):
        self.removeAdditionalColumns(self.datasource)
        
        geom = self.node.xpath("//*[local-name() = '"+self.datasource.geom_col+"']/*")
        geomData = etree.tostring(geom[0], pretty_print=True)
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../resources/transaction/transactions_%s.xsl" % self.datasource.type)
        transform = etree.XSLT(xslt)
        
        result = transform(self.node,
                           datasource="'"+self.datasource.type+"'",
                           transactionType="'"+self.type+"'",
                           geometryAttribute="'"+self.datasource.geom_col+"'",
                           geometryData="'"+geomData+"'",
                           tableName="'"+self.datasource.layer+"'")
        elements = result.xpath("//Statement")
        if len(elements) > 0:
            pattern = re.compile(r'\s+')
            self.set_statement(re.sub(pattern, ' ', str(elements[0])))
            return
        self.set_statement(None)
        
        