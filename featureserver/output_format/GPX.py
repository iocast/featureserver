'''
Created on Jul 30, 2011

@author: michel
'''

from OutputFormat import OutputFormat
import FeatureServer.VectorFormats.Formats.GPX

class GPX(OutputFormat):
    def encode(self, results):
        gpx = FeatureServer.VectorFormats.Formats.GPX.GPX(layername=self.datasources[0])
        
        output = gpx.encode(results)
        return ("application/xml", output, None, 'utf-8')
        