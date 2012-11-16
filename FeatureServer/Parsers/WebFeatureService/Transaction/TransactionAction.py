'''
Created on Oct 16, 2011

@author: michel
'''
import os, re
from lxml import etree
from copy import deepcopy

from FeatureServer.Parsers.WebFeatureService.FilterEncoding.FilterEncoding import FilterEncoding

class TransactionAction(object):
    ''' represents a <wfs:Insert/>, <wfs:Update/> or <wfs:Delete/> '''
        
    def __init__(self, node, transaction, **kwargs):
        super(TransactionAction, self).__init__(**kwargs)
        self.children = []
        self.index = 0
        self.stmt = None
        self.type = ''
        self.node = node
        self.transaction = transaction
    
    
    def set_statement(self, stmt):
        self.stmt = stmt
    
    def get_statement(self):
        if self.stmt == None:
            self.create_statement()
        return self.stmt
    
    def create_statement(self): pass
    
    def get_filter(self):
        ''' returns the filter as string in the datasource format '''
        filters = self.node.xpath("//*[local-name() = 'Filter']")
        if len(filters) == 0:
            return None
        
        filter_node = deepcopy(filters[0])

        filter_encoding = FilterEncoding(etree.tostring(filter_node))
        filter_encoding.parse()
                
        return filter_encoding.render(self.datasource)

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        self.index = 0
        return self
    
    def next(self):
        if self.index >= len(self):
            raise StopIteration
        child = self.children[self.index]
        self.index += 1
        return child
        
    def get(self, index):
        return self.children[index]
    
    def hasChildren(self):
        if len(self) > 0:
            return True

    def getChildren(self):
        return self.children
    
    def appendChild(self, node):
        self.children.append(node)
        
    def getName(self):
        return str(self.node.tag)
    
    def removeAdditionalColumns(self, datasource):
        #filter out additional cols (they can not be saved)
        if hasattr(datasource, "additional_cols"):
            for additional_col in datasource.additional_cols.split(';'):            
                name = additional_col
                matches = re.search('(?<=[ ]as[ ])\s*\w+', str(additional_col))
                if matches:
                    name = matches.group(0)
                
                nodes = self.node.xpath("//*[local-name()='"+name+"']")
                if len(nodes) > 0:
                    for node in nodes:
                        self.node.remove(node)

