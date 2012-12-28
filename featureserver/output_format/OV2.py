'''
Created on Jul 30, 2011

@author: michel
'''

from OutputFormat import OutputFormat
import FeatureServer.VectorFormats.Formats.OV2

class OV2(OutputFormat):
    def encode(self, results):
        ov2 = FeatureServer.VectorFormats.Formats.OV2.OV2(layername=self.datasources[0])
        
        output = ov2.encode(results)

        headers = {
            'Accept': '*/*',
            'Content-Disposition' : 'attachment; filename=poidownload.ov2',
            'Content-Transfer-Encoding' : 'binary'
        }
        
        return ("application/octet-stream", output, headers, '')
        