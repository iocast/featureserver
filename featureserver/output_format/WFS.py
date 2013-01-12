
from OutputFormat import OutputFormat
from ..parsers.WebFeatureService.Response.TransactionResponse import TransactionResponse

from ..vectorformats.wfs import WFS as WFSFormat

class WFS(OutputFormat):
    def encode(self, results):
        wfs = WFSFormat(self.service)
        
        if isinstance(results, TransactionResponse):
            return ("text/xml", wfs.encode_transaction(results), None, 'utf-8')
        
        output = wfs.encode(results)
        return ("text/xml", output, None, 'utf-8')
    
    def encode_exception_report(self, exceptionReport):
        wfs = WFSFormat(self.service)
        return ("text/xml", wfs.encode_exception_report(exceptionReport), None, 'utf-8')

    def get_capabilities(self):
        wfs = WFSFormat(service=self.service)
        return ("text/xml", wfs.get_capabilities(), None, 'utf-8')
    
    def describe_feature_type(self):
        wfs = WFSFormat(service=self.service)
        return ("text/xml; subtype=gml/3.1.1", wfs.describe_feature_type(), None, 'utf-8')
    