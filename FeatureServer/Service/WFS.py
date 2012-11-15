
from Service import Service

from FeatureServer.Exceptions.MissingParameterException import MissingParameterException
from FeatureServer.Exceptions.LayerNotFoundException import LayerNotFoundException

from WebRequest.Actions.Action import Action
from FeatureServer.Parsers.WFSParser import WFSParser

class WFS(Service):

    def __init__(self, request):
        super(WFS, self).__init__(request)
        
        self._service       = "WFS"
        self._actions        = []
        
        # { typename : list(Service.Action), ... }
        self._datasources   = {}
        
        self._version       = ""
        self._operation     = ""
    
    
    def find_typenames(self): pass
    

    def parse(self):
        exceptions = []
        
        # 'request' is mandatory
        self.find_operation()
        
        # do mandatory parameter checks for all operations except "GetCapabilities"
        if self.operation != "GetCapabilities":
            # 'version' is mandatory
            self.find_version()
    
            if self.version[:1] == "1":
                from WFS_V1 import WFS_V1
                self.__class__ = WFS_V1
            elif self.version[:1] == "2":
                from WFS_V2 import WFS_V2
                self.__class__ = WFS_V2
    
            self.find_typenames()
            exceptions.extend(self.check_typenames())
        
        # 'ouputFormat' is optional because set by configuration file
        self.find_output_format()
    
    
        self.create_actions()
    
        return exceptions
    
    
    def find_operation(self):
        # check POST data
        if self.request.post_xml is not None:
            if len(self.post_xml.xpath("/*[local-name() = 'GetCapabilities']")) > 0:
                self._operation = "GetCapabilities"
            elif len(self.post_xml.xpath("/*[local-name() = 'DescribeFeatureType']")) > 0:
                self._operation = "DescribeFeatureType"
            elif len(self.post_xml.xpath("/*[local-name() = 'Transaction']")) > 0:
                self._operation = "Transaction"
            elif len(self.post_xml.xpath("/*[local-name() = 'GetFeature']")) > 0:
                self._operation = "GetFeature"
        
        # check GET params
        if self.request.params.has_key('request'):
            self._operation = self.request.params['request']
        
        # not found
        if len(self.operation) == 0:
            raise MissingParameterException(locator = "Service/" + self.__class__.__name__, parameter = "request")

    def find_version(self):
        # check POST data
        if self.request.post_xml is not None:
            if 'version' in self.request.post_xml.attrib:
                self._version = self.request.post_xml.attrib['version']
                return
        
        # check GET params
        if self.request.params.has_key('version'):
            self._version = str(self.request.params['version'])
            return
        
        # not found
        if len(self.version) == 0:
            raise MissingParameterException(locator = "Service/" + self.__class__.__name__, parameter = "version")


    def check_typenames(self):
        exceptions = []
        for typename in self.datasources.keys():
            if not self.request.server.datasources.has_key(typename):
                exceptions.append(LayerNotFoundException(locator = self.__class__.__name__, layer = typename, layers = self.request.server.datasources.keys()))
    
        return exceptions

    def find_output_format(self):
        # check POST data
        if self.request.post_xml is not None:
            if 'outputFormat' in self.post_xml.attrib:
                self.output_format = self.supported_formats[self.request.post_xml.attrib['outputformat'].lower()]
                return
        
        # check GET params
        if self.request.params.has_key('outputformat'):
            if self.request.params['outputformat'].lower() in self.supported_formats:
                self.output_format = self.supported_formats[self.output_format.params['outputformat'].lower()]
                return
        
        # check file extension in URL
        if len(self.request.path) > 1:
            path_pieces = self.request.path[-1].split(".")
            if len(path_pieces) > 1:
                if path_pieces[-1].lower() in self.supported_formats:
                    self.output_format = self.supported_formats[path_pieces[-1].lower()]
                    return

        # check meta data (last try)
        try:
            self.output_format = self.request.server.metadata_output
        except Exception as e:
            # everythings fail use WFS as defualt
            self.output_format = "WFS"


    def create_actions(self):
        if self.operation == "GetCapabilities":
            self.actions.append(Action(method = "get_capabilities", datasource=None))
            return
        
        if self.operation == "DescribeFeatureType":
            self.actions.append(Action(method="describe_feature_type", datasource=None))
            return
        
        parser = WFSParser(self)
        parser.parse()
    
        actions = parser.get_actions()
    
        for action in actions:
            self.datasources[action.datasource.name].append(action)
    

    @property
    def name(self):
        return self._service
    @property
    def actions(self):
        return self._actions
    @property
    def datasources(self):
        return self._datasources
    @property
    def version(self):
        return self._version
    @property
    def operation(self):
        return self._operation
    