'''
Created on Jul 30, 2011

@author: michel
'''

from OutputFormat import OutputFormat
from vectorformats.formats.ov2 import OV2 as OV2Format

class OV2(OutputFormat):
    def encode(self, results):
        ov2 = OV2Format(layername=self.datasources[0])
        
        output = ov2.encode(results)

        headers = {
            'Accept': '*/*',
            'Content-Disposition' : 'attachment; filename=poidownload.ov2',
            'Content-Transfer-Encoding' : 'binary'
        }
        
        return ("application/octet-stream", output, headers, '')
        