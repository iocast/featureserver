from OutputFormat import OutputFormat
import vectorformats.Formats.GeoRSS

class GeoRSS(OutputFormat):
    def encode_metadata(self, action):
        layers = self.service.datasources
        layer_text = []
        for layer in layers.keys():
            layer_text.append("<collection href='%s/%s/all.atom'><atom:title>%s</atom:title></collection>" % (self.host, layer, layer))
            
        action.metadata = """<?xml version="1.0" encoding="utf-8"?>
<service xmlns="http://www.w3.org/2007/app" xmlns:atom="http://www.w3.org/2005/Atom">
  <workspace>
    <atom:title>FeatureServer</atom:title>
    %s
  </workspace>
</service>
""" % ("\n".join(layer_text))
        return ("application/rss+xml", action.metadata, None)
    
    def encode(self, result):
        atom = vectorformats.Formats.GeoRSS.GeoRSS(url=self.host, feedname=self.datasources[0]) 
        results = atom.encode(result)
        return ("application/atom+xml", results, None, 'utf-8')
    
    def parse(self, params, path_info, host, post_data, request_method):
        self.get_layer(path_info, params)

        atom = vectorformats.Formats.GeoRSS.GeoRSS(url=self.host, feedname=self.datasources[0]) 
        Request.parse(self, params, path_info, host, post_data, request_method, format_obj = atom) 
            
    def encode_exception_report(self, exceptionReport):
        atom = vectorformats.Formats.GeoRSS.GeoRSS(url=self.host) 
        return ("application/atom+xml", atom.encode_exception_report(exceptionReport), None, 'utf-8')
