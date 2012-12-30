'''
Created on Jul 30, 2011

@author: michel
'''

from OutputFormat import OutputFormat
from vectorformats.formats.gpx import GPX as GPXFormat

class GPX(OutputFormat):
    def encode(self, results):
        gpx = GPXFormat(layername=self.datasources[0])
        
        output = gpx.encode(results)
        return ("application/xml", output, None, 'utf-8')
        