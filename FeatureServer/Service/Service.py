
class Service(object):
    _supported_formats = {
        'application/gml+xml; version=3.2' : 'WFS',
        'application/gml+xml; version=3.1' : 'WFS',
        'application/gml+xml; version=2.1' : 'WFS',
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
    

    def __init__(self, request):
        self._request = request
        
        self._output_format = ""
        self._output = None

    def parse(self): pass

    @property
    def request(self):
        return self._request
    
    @property
    def supported_formats(self):
        return self._supported_formats

    @property
    def output_format(self):
        return self._output_format
    @output_format.setter
    def output_format(self, output_format):
        self._output_format = output_format
        
        output_module = __import__("FeatureServer.OutputFormat.%s" % self.output_format, globals(), locals(), self.output_format)
        output_cls = getattr(output_module, self.output_format)
        self._output = output_cls(self)

    @property
    def output(self):
        return self._output

    @property
    def name(self):
        return self.__class__.__name__

