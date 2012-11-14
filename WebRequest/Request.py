
from lxml import etree, objectify
import urlparse

from FeatureServer.Exceptions.LayerNotFoundException import LayerNotFoundException
from FeatureServer.Exceptions.MissingParameterException import MissingParameterException
from WebRequest.Actions.Action import Action

class Request(object):
    
    _type = None
    
    _content_types = {
        'application/vnd.google-earth.kml+xml': 'KML',
        'application/json': 'GeoJSON',
        'text/javascript': 'GeoJSON',
        'application/rss+xml': 'GeoRSS',
        'text/html': 'HTML',
        'osm': 'OSM',
        'gml': 'WFS',
        'wfs': 'WFS',
        'kml': 'KML',
        'json': 'GeoJSON',
        'georss': 'GeoRSS',
        'atom': 'GeoRSS',
        'html': 'HTML',
        'geojson':'GeoJSON',
        'shp': 'SHP',
        'csv': 'CSV',
        'gpx': 'GPX',
        'ov2': 'OV2',
        'spatiallite': 'SpatialLite',
        'dxf' : 'DXF'
    }
    
    _service        = ""
    # { typename : list(Service.Action), ... }
    _datasources    = {}
    _version        = ""
    _actions        = []

    _server    = None

    _post_xml  = None
    _post_kvp  = []
    

    def __init__(self, base_path="", path_info="/", params={}, request_method = "GET", post_data = None,  accepts = ""):
        self._base_path      = base_path
        self._path_info      = path_info
        self._params         = params
        self._request_method = request_method.upper()
        self._post_data      = post_data
        self._accepts        = accepts

    def identify_type(self):
        if self.post_data is not None:
            self.parse_post_data()
        
        if len(self.post_kvp) > 0:
            import KVPRequest
            self.__class__ = KVPRequest.KVPRequest
            return

        import WFSRequest
        self.__class__ = WFSRequest.WFSRequest


    def parse_post_data(self):
        parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
        self._post_xml = etree.XML(self.post_data, parser=parser)
        try:
            parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
            self._post_xml = etree.XML(self.post_data, parser=parser)
        except etree.ParseError as e:
            self._post_kvp = urlparse.parse_qsl(self.post_data)


    def parse(self, server):
        self._server = server
        exceptions = []
        
        # if post data is not empty parse it
        if self.post_data is not None and self.post_xml is not None:
            self.parse_post_data()
        
        # try to find the request
        self.find_request()
        
        # try to find the service
        self.find_service()

        # try to find typename (datasource)
        self.find_typenames()
        exceptions.extend(self.check_typenames())

        # try to find version
        self.find_version()

        # define request type
        self.define_type()

        # create actions
        self.create_actions()

        return exceptions
    

    def find_request(self): pass

    def find_service(self):
        # check accepts (content type)
        if self.accepts is not None:
            if self.accepts.lower() in self.content_types:
                self.service = self.content_types[self.accepts.lower()]
                return
        
        # check meta data (last try)
        try:
            self.service = self.server.metadata_service
        except Exception as e:
            # everythings fail use WFS as defualt
            self.service = "WFS"
        
               
    # TODO: Check that a typename is not inserted double. If so return a exception
    def find_typenames(self):
        ''' TypeNames are layers or in the configuration file defined datasources. '''
        pass

    def check_typenames(self):
        exceptions = []
        for typename in self.datasources.keys():
            if not self.server.datasources.has_key(typename):
                exceptions.append(LayerNotFoundException(locator = self.__class__.__name__, layer = typename, layers = self.server.datasources.keys()))

        return exceptions
    

    def find_version(self): pass


    def define_type(self):
        if self.method == "GET" or (self.method == "OPTIONS" and (self.post_data is None or len(self.post_data) <= 0)):
            self._type = 'selection'
        
        elif self.method == "POST" or self.method == "PUT" or self.method == "DELETE" or (self.method == "OPTIONS" and len(self.post_data) > 0):
            self._type = 'transaction'
        

    def create_actions(self):
        if self.params.has_key("request") and self.params["request"].lower() == "describefeaturetype":
            if not self.params.has_key("typename") and len(self.datasources) == 0:
                raise MissingParameterException(locator=self.__class__.__name__, parameter="typeName")
            
            self.actions.append(Action(method="describe_feature_type", datasource=None))
            return
        
        if len(self.datasources) == 0 or self.params.has_key("request") and self.params["request"].lower() == "getcapabilities":
            self.actions.append(Action(method = "get_capabilities", datasource=None))
            return


    @property
    def type(self):
        return self._type
    
    @property
    def server(self):
        return self._server

    @property
    def post_xml(self):
        return self._post_xml
    @property
    def post_kvp(self):
        return self._post_kvp

    @property
    def host(self):
        return self._base_path
    @property
    def path(self):
        return self.path_info.split("/")
    @property
    def path_info(self):
        return self._path_info
    @property
    def params(self):
        return self._params
    @property
    def method(self):
        return self._request_method
    @property
    def post_data(self):
        return self._post_data
    @property
    def accepts(self):
        return self._accepts
    @property
    def content_types(self):
        return self._content_types

    @property
    def actions(self):
        ''' special actions does not belong to any datasource (layer) '''
        return self._actions
    @actions.setter
    def actions(self, actions):
        self._actions = actions

    @property
    def service(self):
        return self._service
    @service.setter
    def service(self, service):
        self._service = service
    
    @property
    def datasources(self):
        return self._datasources
    @datasources.setter
    def datasources(self, datasources):
        self._datasources = datasources

    @property
    def version(self):
        return self._version
    @version.setter
    def version(self, version):
        self._version = version
