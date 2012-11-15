
from lxml import etree, objectify

from FeatureServer.Exceptions.ServiceNotFoundException import ServiceNotFoundException


class Request(object):

    def __init__(self, base_path="", path_info="/", params={}, request_method = "GET", post_data = None,  accepts = ""):
        self._base_path      = base_path
        self._path_info      = path_info
        self._params         = params
        self._request_method = request_method.upper()
        self._post_data      = post_data
        self._accepts        = accepts
        
        # init class variables
        self._server        = None
        self._service       = None

        self._post_xml      = None


    def parse(self, server):
        self._server = server
        
        # parsing POST data
        if self.post_data is not None:
            self.parse_post_data()

        # determine requested service
        service_name = self.find_service_name()
        try:
            service_module = __import__("FeatureServer.Service.%s" % service_name, globals(), locals(), service_name)
            service_cls = getattr(service_module, service_name)
            self._service = service_cls(self)
        except Exception as e:
            raise ServiceNotFoundException(locator = self.__class__.__name__, service = service_name)

        # do service specific parsing
        self.service.parse()
    

    def parse_post_data(self):
        try:
            parser = objectify.makeparser(remove_blank_text=True, ns_clean=True)
            self._post_xml = etree.XML(self.post_data, parser=parser)
        except etree.ParseError as e:
            pass
    

    def find_service_name(self):
        service_name = None
        # first parameter in the path http://featureserver.org/wfs/
        if len(self.path[1]) > 0:
            service_name = self.path[1].upper()
        
        # check if parameter 'SERVICE' is set
        elif self.params.has_key('service'):
            service_name = self.params['service'].upper()

        # check post data
        else:
            if self.post_xml is not None:
                if 'service' in self.post_xml.attrib:
                    service_name = self.post_xml.attrib['service'].upper()
                
        
        return service_name


    @property
    def server(self):
        return self._server
    @property
    def service(self):
        return self._service

    @property
    def post_xml(self):
        return self._post_xml

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
