
from OutputFormat import OutputFormat
from vectorformats.formats.geojson import GeoJSON as GeoJSONFormat

class GeoJSON(OutputFormat):
    
    def get_capabilities(self):
        callback = None
        if 'callback' in self.service.request.params:
            callback = self.service.request.params['callback']
        
        geojson = GeoJSONFormat(self.service, callback = callback)
        return ("text/plain", geojson.get_capabilities())
    
    
    def describe_feature_type(self):
        callback = None
        if 'callback' in self.service.request.params:
            callback = self.service.request.params['callback']

        geojson = GeoJSONFormat(self.service, callback = callback)
        return ("text/plain", geojson.describe_feature_type())
    

    def parse(self, params, path_info, host, post_data, request_method, format_obj=None):
        if 'callback' in params:
            self.callback = params['callback']
        g = GeoJSONFormat()
        Request.parse(self, params, path_info, host, post_data, request_method, format_obj=g)

    def encode(self, result):
        g = GeoJSONFormat()
        result = g.encode(result)
        
        if self.datasources[0]:
            datasource = self.service.datasources[self.datasources[0]]
        
        if self.callback and datasource and hasattr(datasource, 'gaping_security_hole'):
            return ("text/plain", "%s(%s);" % (self.callback, result), None, 'utf-8')
        else:
            return ("text/plain", result, None, 'utf-8')

    def encode_exception_report(self, exceptionReport):
        geojson = GeoJSONFormat()
        return ("text/plain", geojson.encode_exception_report(exceptionReport), None, 'utf-8')
