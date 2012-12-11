'''
Created on Oct 16, 2011

@author: michel
'''
import os, re
from lxml import etree

from TransactionAction import TransactionAction
from FeatureServer.WebRequest.Actions.Delete import Delete as DeleteAction

class Delete(TransactionAction, DeleteAction):
    
    def __init__(self, datasource, node, transaction):
        super(Delete, self).__init__(datasource=datasource, node=node, transaction=transaction)
        self.type = 'delete'
        
    def create_statement(self):
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../assets/transformation/transaction/transactions_%s.xsl" % self.datasource.type)
        transform = etree.XSLT(xslt)
        
        result = transform(self.node,
                           version          = "'" + str(self.transaction.service.version) + "'",
                           transactionType  = "'" + self.type + "'",
                           tableName        = "'" + self.datasource.layer + "'" )

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
        
        