'''
Created on Dec 10, 2011

@author: michel
'''
import re
from lxml import etree, objectify
from copy import deepcopy

from parser import Parser
from ..web_request.operators import Constraint, Sort


from .web_feature_service.filter_encoding.select import Select
from .web_feature_service.transaction.Transaction import Transaction




class WFSParser(Parser):
    ''' parses WFS-T and WFS GetFeature operations '''
    
    def __init__(self, service):
        Parser.__init__(self, service)
    
    def parse(self): pass
    
    def add_action(self, action):
        self.service.datasources[action.datasource.name].append(action)
    def add_actions(self, actions):
        for action in actions:
            self.service.datasources[action.datasource.name].append(action)



    def parse_sort(self):
        sort = []
        
        if "sort" in self.service.request.params:
            sort_list = self.service.request.params['sortby'].split(",")
            for item in sort_list:
                attribute, operator = item.split("_")
                sort.append(Sort(attribute=attribute, operator=operator))
        
        return sort
    
    def parse_constraints(self):
        constraints = []
        
        if "queryable" in self.service.request.params:
            query_list = self.service.request.params['queryable'].split(",")
            
            for query in query_list:
                for key, value in self.service.request.params.iteritems():
                    if "__" in key:
                        attribute, operator = key.split("__")
                        if query == attribute:
                            constraints.append(Constraint(attribute=attribute, value=self.service.request.params[key], operator=operator))
        
        return constraints

    def parse_sort(self):
        sort_list = []
        
        if "sortby" in self.service.request.params:
            list = self.service.request.params['sortby'].split(",")
            for item in list:
                attribute, operator = item.split("_")
                sort_list.append(Sort(attribute=attribute, operator=operator))

        return sort_list



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
                    # check if query as a filter node
                    filters = self.service.request.post_xml.xpath("./*[local-name() = 'Filter']")
                    if len(filters) > 0:
                        # filter child node found
                        self.add_action(self.parse_filter(datasource=self.service.request.server.datasources[query.attrib['typeName']], dom=deepcopy(filters[0]), properties=self.parse_query_property_names(deepcopy(query))))
                    else:
                        self.add_action(self.parse_without_filter(datasource=self.service.request.server.datasources[query.attrib['typeName']]))
                    
            
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
                        self.add_action(self.parse_without_filter(datasource=self.service.request.server.datasources[typename]))
            
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
        return Select(datasource=datasource, data=None, service=self.service, ids=ids, attributes=properties, constraints=self.parse_constraints(), sort=self.parse_sort())
    
    def parse_filter(self, datasource, dom, properties=[]):
        ''' parses a OGC <wfs:Filter/> tag '''
        return Select(datasource=datasource, data=etree.tostring(dom), service=self.service, attributes=properties, constraints=self.parse_constraints(), sort=self.parse_sort())
    
    def parse_transaction(self, dom):
        ''' parses the whole <wfs:Transaction/> and returns a list of actions '''
        transaction = Transaction(self.service)
        transaction.parse(etree.tostring(dom))
        return transaction.getActions()




class WFS_V2_Parser(WFSParser):
    
    def __init__(self, service):
        super(WFS_V2_Parser, self).__init__(service)
    
    def parse(self):
        try:
            # try to parse post data:
            parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
            dom = etree.XML(self.service.request.post_data, parser=parser)
            
            if len(dom.xpath("/*[local-name() = 'GetFeature']")) > 0:
                print "POST Query"
                queries = dom.xpath("/*[local-name() = 'GetFeature']/*[local-name() = 'Query'][@typeNames]")
                
                for query in queries:
                    typenames = query.attrib['typeNames'].split(" ")
                    if len(typenames) == 1:
                        self.actions.append(self.parse_filter(datasource=self.service.request.server.datasources[typenames[0]], dom=deepcopy(query.xpath("./*[local-name() = 'Filter']")[0]), properties=self.parse_query_property_names(deepcopy(query))))
                    elif len(typenames) > 1:
                        #TODO: join query
                        print("join query")
            
            
            elif len(dom.xpath("/*[local-name() = 'Transaction']")) > 0:
                print "POST Transaction"
                # Transaction is only in POST mode possible
                # TODO: raise exception if request.type is not 'transaction'
                
                # WFS transaction can only be handled as a whole
                self.actions.extend(self.parse_transaction(dom))
        
        except Exception as e:
            # try to parse filter parameter(s)
            typenames = self.service.request.params['typenames'].split(",")
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
                    
                    self.actions.append(self.parse_filter(datasource=self.service.request.server.datasources[self.service.request.params['typenames']], dom=deepcopy(dom)))
                except Exception as e:
                    print "no filter"
                    # no filter is set (query all)
                    self.actions.append(self.parse_without_filter(datasource=self.service.request.server.datasources[self.service.request.params['typenames']]))
    
    
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

