

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
        try:
            # try to parse post data:
            parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
            dom = etree.XML(self.service.request.post_data, parser=parser)
            
            if len(dom.xpath("/*[local-name() = 'GetFeature']")) > 0:
                print "POST Query"
                queries = dom.xpath("/*[local-name() = 'GetFeature']/*[local-name() = 'Query'][@typeName]")
                
                for query in queries:
                    self.actions.append(self.parse_filter(datasource=self.service.request.server.datasources[query.attrib['typeName']], dom=deepcopy(query.xpath("./*[local-name() = 'Filter']")[0]), properties=self.parse_query_property_names(deepcopy(query))))
            
            elif len(dom.xpath("/*[local-name() = 'Transaction']")) > 0:
                print "POST Transaction"
                # Transaction is only in POST mode possible
                # TODO: raise exception if request.type is not 'transaction'
                
                # WFS transaction can only be handled as a whole
                self.actions.extend(self.parse_transaction(dom))
        
        except Exception as e:
            # try to parse filter parameter(s)
            typenames = self.service.request.params['typename'].split(",")
            if len(typenames) > 1:
                print "GET more than 1 filter"
                if self.service.request.params.has_key('filter'):
                    for (i, filter) in enumerate(re.findall(r'\((.*?)\)', self.service.request.params['filter'])):
                        try:
                            parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
                            dom = etree.XML(filter, parser=parser)
                            
                            print "    - filter found: " + str(typenames[i])
                            
                            self.actions.append(self.parse_filter(datasource=self.service.request.server.datasources[typenames[i]], dom=deepcopy(dom)))
                        except Exception as e:
                            # no filter is set (query all)
                            print "    - filter not found: " + str(typenames[i])
                            self.actions.append(self.parse_without_filter(datasource=self.service.request.server.datasources[typenames[i]]))
                else:
                    for typename in typenames:
                        print "    - filter not found: " + str(typename)
                        self.actions.append(self.parse_without_filter(datasource=self.service.request.server.datasources[typename]))
    
            else:
                try:
                    print "GET 1 filter"
                    parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
                    dom = etree.XML(self.service.request.params['filter'], parser=parser)
                    
                    self.actions.append(self.parse_filter(datasource=self.service.request.server.datasources[self.service.request.params['typename']], dom=deepcopy(dom)))
                except Exception as e:
                    print "no filter"
                    # no filter is set (query all)
                    self.actions.append(self.parse_without_filter(datasource=self.service.request.server.datasources[self.service.request.params['typename']]))

    
    def parse_query_property_names(self, dom):
        ''' parses <wfs:PropertyName/> in a OGC FE XML '''
        return [str(property.text) for property in dom.xpath("/*[local-name() = 'Query']/*[local-name() = 'PropertyName']")]
    
    def parse_without_filter(self, datasource, properties=[]):
        ''' creates a select action which should return all records of a datasource '''
        import FeatureServer.WebRequest.Actions.Select
        return FeatureServer.WebRequest.Actions.Select.Select(datasource=datasource)
    
    def parse_filter(self, datasource, dom, properties=[]):
        ''' parses a OGC <wfs:Filter/> tag '''
        return Select(datasource=datasource, data=etree.tostring(dom), properties=properties, service=self.service)
    
    def parse_transaction(self, dom):
        ''' parses the whole <wfs:Transaction/> and returns a list of actions '''
        transaction = Transaction(self.service)
        transaction.parse(etree.tostring(dom))
        return transaction.getActions()

