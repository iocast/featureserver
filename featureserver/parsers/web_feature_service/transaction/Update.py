'''
Created on Oct 16, 2011

@author: michel
'''
import os, re
from lxml import etree

from TransactionAction import TransactionAction
from featureserver.web_request.actions import Update as UpdateResult


class Update(TransactionAction, UpdateResult):
    
    def __init__(self, datasource, node, transaction):
        super(Update, self).__init__(datasource=datasource, node=node, transaction=transaction)
        self.type = 'update'
        
    def create_statement(self):
        self.removeAdditionalColumns(self.datasource)
        
        geom = self.node.xpath("//*[local-name() = 'Name' and text()='"+self.datasource.geom_col+"']/following-sibling::*[1]/*")
        geomData = ''
        if len(geom) > 0:
            geomData = etree.tostring(geom[0], pretty_print=True)
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../assets/transformation/transaction/transactions_%s.xsl" % self.datasource.type)
        
        
        from ..extensions import lxml_xpath as xpath_ext
        from ..extensions import lxml_xslt as xslt_ext
        ext_module = xpath_ext.PostGISHstoreExtension(self.datasource)
        functions = ('hstore_attribute', 'is_hstore', 'clip_hstore')
        extensions = etree.Extension( ext_module, functions, ns='http://featureserver.org' )
    
        transform = etree.XSLT(xslt, extensions=extensions)

        result = transform(self.node,
                           version              = "'" + str(self.transaction.service.version) + "'",
                           transactionType      = "'" + self.type + "'",
                           geometryAttribute    = "'" + self.datasource.geom_col + "'",
                           geometryData         = "'" + geomData + "'",
                           tableName            = "'" + self.datasource.layer + "'")
        
        elements = result.xpath("//Statement")
        #print elements
        if len(elements) > 0:
            pattern = re.compile(r'\s+')
            
            stmt = re.sub(pattern, ' ', str(elements[0]))
            filter = super(Update, self).get_filter()
            
            if filter is not None:
                stmt += filter
            
            self.set_statement(stmt)
            return
        self.set_statement(None)
        
        