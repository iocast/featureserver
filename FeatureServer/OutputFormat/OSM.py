from OutputFormat import OutputFormat
import vectorformats.Formats.OSM

class OSM(OutputFormat):
    def encode(self, result):
        osm = vectorformats.Formats.OSM.OSM()
        
        results = osm.encode(result)
        
        return ("application/xml", results, None, 'utf-8')
        