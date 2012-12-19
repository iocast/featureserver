

from WFSParser import WFSParser
from WebFeatureService.FilterEncoding.Select import Select
from WebFeatureService.Transaction.Transaction import Transaction

import re
from lxml import etree, objectify
from copy import deepcopy

class WFS_V1_Parser(WFSParser):

    def __init__(self, service):
        super(WFS_V1_Parser, self).__init__(service)

    def parse(self):
        # POST data is set as filter
        if self.service.request.post_xml is not None:
            if self.service.operation == "GetFeature":
                # TODO: maybe loop over self.service.datasources instead of dom
                queries = self.service.request.post_xml.xpath("/*[local-name() = 'GetFeature']/*[local-name() = 'Query'][@typeName]")
                for query in queries:
                    self.add_action(self.parse_filter(datasource=self.service.request.server.datasources[query.attrib['typeName']], dom=deepcopy(query.xpath("./*[local-name() = 'Filter']")[0]), properties=self.parse_query_property_names(deepcopy(query))))
        
            elif self.service.operation == "Transaction":
                # Transaction is only in POST mode possible
                # TODO: raise exception if request.type is not 'transaction'
                
                # WFS transaction can only be handled as a whole
                self.add_actions(self.parse_transaction(dom))
        
        
        # try to parse parameters
        if self.service.request.params.has_key('typename'):
            typenames = self.service.request.params['typename'].split(",")
            # multiple layers
            if len(typenames) > 1:
                if self.service.request.params.has_key('filter'):
                    for (i, filter) in enumerate(re.findall(r'\((.*?)\)', self.service.request.params['filter'])):
                        try:
                            parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
                            dom = etree.XML(filter, parser=parser)
                        
                            self.add_action(self.parse_filter(datasource=self.service.request.server.datasources[typenames[i]], dom=deepcopy(dom)))
                        except Exception as e:
                            # no filter is set (query all)
                            self.add_action(self.parse_without_filter(datasource=self.service.request.server.datasources[typenames[i]]))
            
                # no filter exists. create for each typename a empty filter = query all
                else:
                    for typename in typenames:
                        self.add_action(self.actions.append(self.parse_without_filter(datasource=self.service.request.server.datasources[typename])))
        
            # single layer
            elif len(typenames) == 1:
                if self.service.request.params.has_key('filter'):
                    parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
                    dom = etree.XML(self.service.request.params['filter'], parser=parser)
    
                    self.add_action(self.parse_filter(datasource=self.service.request.server.datasources[self.service.request.params['typename']], dom=deepcopy(dom)))
            
                else:
                    self.add_action(self.parse_without_filter(datasource=self.service.request.server.datasources[self.service.request.params['typename']]))

    
        # check if layer exists in path name
        if len(self.service.request.path) > 2:
            
            # check if file name exists
            path_pieces = self.service.request.path[-1].split(".")
            if len(path_pieces) > 0:
                # file name is a keyword
                if path_pieces[0].lower() in self.service.supported_keywords.keys():
                    if self.service.request.params.has_key('filter'):
                        parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
                        dom = etree.XML(self.service.request.params['filter'], parser=parser)
                        
                        self.add_action(self.parse_filter(datasource=self.service.request.server.datasources[str(self.service.request.path[2])], dom=deepcopy(dom)))
                    else:
                        self.add_action(self.parse_without_filter(datasource=self.service.request.server.datasources[str(self.service.request.path[2])]))
                
                # file name is a id
                else:
                    self.add_action(self.parse_without_filter(datasource=self.service.request.server.datasources[str(self.service.request.path[2])], ids=[path_pieces[0]]))
        
        
        # TODO: maybee add for all layers in self.service.datasources a 'query all' action
        else:
            ''' '''
        
    
    def parse_query_property_names(self, dom):
        ''' parses <wfs:PropertyName/> in a OGC FE XML '''
        return [str(property.text) for property in dom.xpath("/*[local-name() = 'Query']/*[local-name() = 'PropertyName']")]
    
    def parse_without_filter(self, datasource, properties=[], ids=[]):
        ''' creates a select action which should return all records of a datasource '''
        #import FeatureServer.WebRequest.Actions.Select
        #return FeatureServer.WebRequest.Actions.Select.Select(datasource=datasource)
        return Select(datasource=datasource, data=None, service=self.service, ids=ids, attributes=properties, constraints=constraints)
    
    def parse_filter(self, datasource, dom, properties=[]):
        ''' parses a OGC <wfs:Filter/> tag '''
        return Select(datasource=datasource, data=etree.tostring(dom), properties=properties, service=self.service)
    
    def parse_transaction(self, dom):
        ''' parses the whole <wfs:Transaction/> and returns a list of actions '''
        transaction = Transaction(self.service)
        transaction.parse(etree.tostring(dom))
        return transaction.getActions()

