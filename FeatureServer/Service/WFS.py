__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: WFS.py 485 2008-05-18 10:51:09Z crschmidt $"

from FeatureServer.Service.Service import Service
from FeatureServer.Parsers.WebFeatureService.Response.TransactionResponse import TransactionResponse

import VectorFormats.Formats.WFS

class WFS(Service):
    def encode(self, results):
        wfs = VectorFormats.Formats.WFS.WFS(self.request)
        
        if isinstance(results, TransactionResponse):
            return ("text/xml", wfs.encode_transaction(results), None, 'utf-8')
        
        output = wfs.encode(results)
        return ("text/xml", output, None, 'utf-8')
    
    def encode_exception_report(self, exceptionReport):
        wfs = VectorFormats.Formats.WFS.WFS(self.request)
        return ("text/xml", wfs.encode_exception_report(exceptionReport), None, 'utf-8')

    def get_capabilities(self):
        wfs = VectorFormats.Formats.WFS.WFS(self.request)
        result = wfs.get_capabilities()
        return ("text/xml", result)
    
    def describe_feature_type(self):
        wfs = VectorFormats.Formats.WFS.WFS(self.request)
        result = wfs.describe_feature_type()
        return ("text/xml; subtype=gml/3.1.1", result)
    