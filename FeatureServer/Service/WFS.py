__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: WFS.py 485 2008-05-18 10:51:09Z crschmidt $"

from FeatureServer.Service import Request
import vectorformats.Formats.WFS
from FeatureServer.Service import NoLayerException
from FeatureServer.Service import Action
from FeatureServer.WebFeatureService.WFSRequest import WFSRequest
from FeatureServer.WebFeatureService.Transaction.TransactionResponse import TransactionResponse

class WFS(Request):
    def encode(self, results):
        wfs = vectorformats.Formats.WFS.WFS(layername=self.datasources[0])
        
        if isinstance(results, TransactionResponse):
            return ("text/xml", wfs.encode_transaction(results), None, 'utf-8')
        
        output = wfs.encode(results)
        return ("text/xml", output, None, 'utf-8')
    
    def encode_exception(self, exceptionReport):
        wfs = vectorformats.Formats.WFS.WFS(layername=self.datasources[0])
        return ("text/xml", wfs.encode_exception(exceptionReport), None, 'utf-8')
        
    def parse(self, params, path_info, host, post_data, request_method):
        self.host = host
        
        try:
            self.get_layer(path_info, params)
        except NoLayerException:
            a = Action()
            
            if params.has_key('service') and params['service'].lower() == 'wfs':
                for layer in self.service.datasources:
                    self.datasources.append(layer)
                if params.has_key('request'):
                    a.request = params['request']
                else:
                    a.request = "GetCapabilities"
            else:
                a.method = "metadata"
            
            self.actions.append(a)
            return
        
        wfsrequest = WFSRequest()
        try:
            Request.parse(self, params, path_info, host, post_data, request_method, format_obj=wfsrequest)
        except:
            raise

    def getcapabilities(self, version):
        wfs = vectorformats.Formats.WFS.WFS(layers=self.datasources, datasources=self.service.datasources, host=self.host)
        result = wfs.getcapabilities()
        return ("text/xml", result)
    
    def describefeaturetype(self, version):
        wfs = vectorformats.Formats.WFS.WFS(layers=self.datasources, datasources=self.service.datasources, host=self.host)
        result = wfs.describefeaturetype()
        return ("text/xml; subtype=gml/3.1.1", result)
    