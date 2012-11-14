'''
Created on Oct 16, 2011

@author: michel
'''
import os, re
from lxml import etree

from TransactionAction import TransactionAction
from WebRequest.Actions.Delete import Delete as DeleteAction

class Delete(TransactionAction, DeleteAction):
    
    def __init__(self, datasource, node):
        super(Delete, self).__init__(datasource=datasource, node=node)
        self.type = 'delete'
        
    def create_statement(self):
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../resources/transaction/transactions.xsl")
        transform = etree.XSLT(xslt)
        
        result = transform(self.node,
                           datasource="'"+self.datasource.type+"'",
                           transactionType="'"+self.type+"'",
                           tableName="'"+self.datasource.layer+"'",
                           tableId="'"+self.datasource.fid_col+"'")
        elements = result.xpath("//Statement")
        if len(elements) > 0:
            pattern = re.compile(r'\s+')
            
            stmt = re.sub(pattern, ' ', str(elements[0]))
            filter = super(Delete, self).get_filter()
            
            if filter is not None:
                stmt += filter
            
            self.set_statement(stmt)
            return
        self.set_statement(None)
        
        