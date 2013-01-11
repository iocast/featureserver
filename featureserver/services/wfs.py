
from service import Service

from ..exceptions.syntax import MissingParameterException, VersionNotSupportedException
from ..exceptions.configuration import LayerNotFoundException

from ..web_request.actions import Action

class WFS(Service):
    '''
        Checks if all required parameters are set as well as paremeter dependencies
    '''
    
    _supported_versions = ["1.1.0", "2.0.0"]
    _supported_keywords = { "capabilities" : "GetCapabilities",
                            "describe" : "DescribeFeatureType",
                            "features" : "GetFeature" }
    _service            = "WFS"

    def __init__(self, request):
        super(WFS, self).__init__(request)
        
        self._actions        = []
        
        # { typename : list(Service.Action), ... }
        self._datasources   = {}
        
        self._version       = ""
        self._operation     = ""

        self._sort          = []
        self._bbox          = []
    
    
 
    def find_typenames(self): pass
    def create_parser(self): pass

    
    def parse(self):
        exceptions = []
        
        # 'request' is mandatory
        self.find_operation()
        
        # do mandatory parameter checks for all operations except "GetCapabilities"
        if self.operation != "GetCapabilities":
            # 'version' is mandatory
            try:
                self.find_version()
            
                if self.version not in self.supported_versions:
                    exceptions.append(VersionNotSupportedException(locator = self.__class__.__name__, version = self.version, supported_versions = self.supported_versions))
    
                if self.version[:1] == "1":
                    from wfs_v1 import WFS_V1
                    self.__class__ = WFS_V1
                elif self.version[:1] == "2":
                    from wfs_v2 import WFS_V2
                    self.__class__ = WFS_V2
            
                self.find_typenames()
                exceptions.extend(self.check_typenames())
            
            except Exception as e:
                # TODO: remove
                raise e
                exceptions.append(e)
        
        # 'ouputFormat' is optional because set by configuration file
        self.find_output_format()
        if len(exceptions) == 0:
            self.create_actions()
        
        return exceptions
    
    
    def find_operation(self):
        # check POST data
        if self.request.post_xml is not None:
            if len(self.request.post_xml.xpath("/*[local-name() = 'GetCapabilities']")) > 0:
                self._operation = "GetCapabilities"
            elif len(self.request.post_xml.xpath("/*[local-name() = 'DescribeFeatureType']")) > 0:
                self._operation = "DescribeFeatureType"
            elif len(self.request.post_xml.xpath("/*[local-name() = 'Transaction']")) > 0:
                self._operation = "Transaction"
            elif len(self.request.post_xml.xpath("/*[local-name() = 'GetFeature']")) > 0:
                self._operation = "GetFeature"
        
        # check GET params
        if self.request.params.has_key('request'):
            self._operation = self.request.params['request']
    
        # check file name
        if len(self.request.path) > 1:
            path_pieces = self.request.path[-1].split(".")
            if len(path_pieces) > 0:
                # file name is a keyword
                if path_pieces[0].lower() in self.supported_keywords.keys():
                    self._operation = self.supported_keywords[path_pieces[0].lower()]
    
                # file name is a id
                else:
                    self._operation = "GetFeature"
    
        
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
                exceptions.append(LayerNotFoundException(locator = self.__class__.__name__, layer = typename, supported_layers = self.request.server.datasources.keys()))
        
        return exceptions

    def find_output_format(self):
        # check POST data
        if self.request.post_xml is not None:
            if 'outputFormat' in self.request.post_xml.attrib:
                self.output_format = self.supported_formats[self.request.post_xml.attrib['outputformat'].lower()]
                return
        
        # check GET params
        if self.request.params.has_key('outputformat'):
            if self.request.params['outputformat'].lower() in self.supported_formats:
                self.output_format = self.supported_formats[self.request.params['outputformat'].lower()]
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
        
        parser = self.create_parser()
        parser.parse()
    
    @property
    def name(self):
        return self._service
    @property
    def supported_versions(self):
        return self._supported_versions
    @property
    def supported_keywords(self):
        return self._supported_keywords
    
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

