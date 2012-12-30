from OutputFormat import OutputFormat
from vectorformats.formats.osm import OSM as OSMFormat

class OSM(OutputFormat):
    def encode(self, result):
        osm = OSMFormat()
        
        results = osm.encode(result)
        
        return ("application/xml", results, None, 'utf-8')
        