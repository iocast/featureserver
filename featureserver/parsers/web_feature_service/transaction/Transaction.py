'''
Created on Oct 16, 2011

@author: michel
'''
import os
import sys
from lxml import etree
from lxml import objectify
from copy import deepcopy

from .TransactionAction import TransactionAction

class Transaction(object):
    ''' parses the whole transaction '''
    
    namespaces = {'gml' : 'http://www.opengis.net/gml',
                  'fs' : 'http://featureserver.org/fs'}
    
    def __init__(self, service) :
        self._service = service
        self._tree = None

    @property
    def available_datasources(self):
        return self.service.request.server.datasources
    @property
    def service(self):
        return self._service
    @property
    def tree(self):
        return self._tree

    def getActions(self):
        return self.tree

    def parse(self, xml):
        self.parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
        
        self.dom = etree.XML(xml, parser=self.parser)
        self.parseDOM()
        
    def parseDOM(self, node = None, transaction = None):
        
        if node == None:
            node = self.dom
            
        if transaction == None:
            transaction = TransactionAction(node=node, transaction=self)
        
        transaction_class = None
        
        for trans in node.iterchildren():
            if str(trans.xpath('local-name()')) == 'Insert':
                # need to be handled specifically because a <wfs:Insert/> statement could have several <typeName/> children
                for child in trans.iterchildren():
                    # handle <typeName/> children
                    transaction_class = self.getTransactionInstance(transaction=str(trans.xpath('local-name()')), typename=str(child.xpath("local-name()")), node=deepcopy(child))
                    transaction.appendChild(transaction_class)
            elif str(trans.xpath('local-name()')) == 'Update' or str(trans.xpath('local-name()')) == 'Delete':
                transaction_class = self.getTransactionInstance(transaction=str(trans.xpath('local-name()')), typename=str(trans.attrib['typeName']), node=deepcopy(trans))
                transaction.appendChild(transaction_class)
            
                    
        self._tree = transaction
            
    def getTransactionInstance(self, transaction, typename, node):
        print ">>> transaction: " + typename
        try:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            transaction_module = __import__(transaction, globals(), locals())
        except ImportError:
            raise Exception("Could not find transaction for %s" % transaction)
        
        transaction_func = getattr(transaction_module, transaction)
        return transaction_func(datasource=self.available_datasources[typename], node=node, transaction=self)
    
    def render(self, datasource, node = None):
        if node == None:
            node = self.tree
            
        self.create(datasource, node)
    
    def create(self, datasource, node):
        for child in node:
            self.create(datasource, child)
        
        node.createStatement(datasource)
        
    def assemble(self, datasource, node, sql = ''):
        for child in node:
            sql += self.assemble(datasource, child, sql)
        
        return sql
        
    def __str__(self, *args, **kwargs):
        return etree.tostring(self.dom, pretty_print = True)
    