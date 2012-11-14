'''
Created on Oct 16, 2011

@author: michel
'''
import os, re
from lxml import etree

from TransactionAction import TransactionAction
from WebRequest.Actions.Update import Update as UpdateResult

class Update(TransactionAction, UpdateResult):
    
    def __init__(self, datasource, node):
        super(Update, self).__init__(datasource=datasource, node=node)
        self.type = 'update'
        
    def create_statement(self):
        self.removeAdditionalColumns(self.datasource)
        
        geom = self.node.xpath("//*[local-name() = 'Name' and text()='"+self.datasource.geom_col+"']/following-sibling::*[1]/*")
        geomData = ''
        if len(geom) > 0:
            geomData = etree.tostring(geom[0], pretty_print=True)
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../resources/transaction/transactions.xsl")
        transform = etree.XSLT(xslt)
        
        result = transform(self.node,
                           datasource="'"+self.datasource.type+"'",
                           transactionType="'"+self.type+"'",
                           geometryAttribute="'"+self.datasource.geom_col+"'",
                           geometryData="'"+geomData+"'",
                           tableName="'"+self.datasource.layer+"'",
                           tableId="'"+self.datasource.fid_col+"'")

        elements = result.xpath("//Statement")
        if len(elements) > 0:
            pattern = re.compile(r'\s+')
            
            stmt = re.sub(pattern, ' ', str(elements[0]))
            filter = super(Update, self).get_filter()
            
            if filter is not None:
                stmt += filter
            
            self.set_statement(stmt)
            return
        self.set_statement(None)
        
        