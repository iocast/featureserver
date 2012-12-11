'''
Created on Jul 30, 2011

@author: michel
'''

from OutputFormat import OutputFormat
import vectorformats.Formats.GPX

class GPX(OutputFormat):
    def encode(self, results):
        gpx = vectorformats.Formats.GPX.GPX(layername=self.datasources[0])
        
        output = gpx.encode(results)
        return ("application/xml", output, None, 'utf-8')
        