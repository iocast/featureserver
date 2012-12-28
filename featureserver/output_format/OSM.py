from OutputFormat import OutputFormat
import FeatureServer.VectorFormats.Formats.OSM

class OSM(OutputFormat):
    def encode(self, result):
        osm = FeatureServer.VectorFormats.Formats.OSM.OSM()
        
        results = osm.encode(result)
        
        return ("application/xml", results, None, 'utf-8')
        