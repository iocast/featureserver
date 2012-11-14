'''
'''

from WebRequest.Request import Request
from FeatureServer.Parsers.WFSParser import WFSParser

class WFSRequest(Request):

    def find_request(self):
        # check POST data
        if self.post_xml is not None:
            if len(self.post_xml.xpath("/*[local-name() = 'GetCapabilities']")) > 0:
                self.params['request'] = "GetCapabilities"
            elif len(self.post_xml.xpath("/*[local-name() = 'DescribeFeatureType']")) > 0:
                self.params['request'] = "DescribeFeatureType"
            elif len(self.post_xml.xpath("/*[local-name() = 'Transaction']")) > 0:
                # TODO: check if correct
                return
            elif len(self.post_xml.xpath("/*[local-name() = 'GetFeature']")) > 0:
                # TODO: check if correct
                return
        # check GET params
        if not self.params.has_key('request'):
            self.params['request'] = "GetCapabilities"
        

    def find_service(self):
        # check POST data
        if self.post_xml is not None:
            if 'service' in self.post_xml.attrib:
                if self.post_xml.attrib['service'].lower() in self.content_types:
                    self.service = self.content_types[self.post_xml.attrib['service'].lower()]
                    return

        # check GET data
        if self.params.has_key('service'):
            if self.params['service'].lower() in self.content_types:
                self.service = self.content_types[self.params['service'].lower()]
                return

        super(WFSRequest, self).find_service()


    def find_typenames(self):
        # check POST data
        if self.post_xml is not None:
            # check if child nodes <wfs:TypeName> exists
            typenames = self.post_xml.xpath("/*[local-name() = 'DescribeFeatureType']/*[local-name() = 'TypeName']")
            if len(typenames) > 0:
                for typename in typenames:
                    self.datasources.update({str(typename.text) : []})
                return
            
            # check if child nodes <wfs:Query typeName=""/> exists
            typenames = self.post_xml.xpath("/*[local-name() = 'GetFeature']/*[local-name() = 'Query']")
            if len(typenames) > 0:
                for typename in typenames:
                    self.datasources.update({typename.attrib['typeName'] : []})
                return
    
            # find typenames in <wfs:Transaction/>
            #    - <wfs:Insert/>
            inserts = self.post_xml.xpath("/*[local-name() = 'Transaction']/*[local-name() = 'Insert']")
            for insert in inserts:
                self.datasources.update({ str(key.xpath("local-name()")) : [] for key in insert.iterchildren() })
            #    - <wfs:Update/>
            #    - <wfs:Delete/>
            nodes = self.post_xml.xpath("/*[local-name() = 'Transaction']/*[local-name() = 'Update' or local-name() = 'Delete']")
            self.datasources.update({ str(node.attrib['typeName']) : [] for node in nodes })
            return
    
        # check GET data
        if self.params.has_key('typename'):
            self.datasources.update({key : [] for key in self.params['typename'].split(",")})
            return


    def find_version(self):
        # check POST data
        if self.post_xml is not None:
            if 'version' in self.post_xml.attrib:
                self.version = self.post_xml.attrib['version']
                return

        # check GET data
        if self.params.has_key('version'):
            self.version = str(self.params['version'])
            return


    def create_actions(self):
        super(WFSRequest, self).create_actions()
        
        if len(self.actions) == 0:
            parser = WFSParser(self)
            parser.parse()
            
            actions = parser.get_actions()
            
            for action in actions:
                self.datasources[action.datasource.name].append(action)
        
