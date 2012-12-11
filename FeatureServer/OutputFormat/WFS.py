__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: WFS.py 485 2008-05-18 10:51:09Z crschmidt $"

from OutputFormat import OutputFormat
from FeatureServer.Parsers.WebFeatureService.Response.TransactionResponse import TransactionResponse

import FeatureServer.VectorFormats.Formats.WFS

class WFS(OutputFormat):
    def encode(self, results):
        wfs = FeatureServer.VectorFormats.Formats.WFS.WFS(self.service)
        
        if isinstance(results, TransactionResponse):
            return ("text/xml", wfs.encode_transaction(results), None, 'utf-8')
        
        output = wfs.encode(results)
        return ("text/xml", output, None, 'utf-8')
    
    def encode_exception_report(self, exceptionReport):
        wfs = FeatureServer.VectorFormats.Formats.WFS.WFS(self.service)
        return ("text/xml", wfs.encode_exception_report(exceptionReport), None, 'utf-8')

    def get_capabilities(self):
        wfs = FeatureServer.VectorFormats.Formats.WFS.WFS(self.service)
        result = wfs.get_capabilities()
        return ("text/xml", result)
    
    def describe_feature_type(self):
        wfs = FeatureServer.VectorFormats.Formats.WFS.WFS(self.service)
        result = wfs.describe_feature_type()
        return ("text/xml; subtype=gml/3.1.1", result)
    