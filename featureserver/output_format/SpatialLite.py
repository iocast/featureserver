'''
Created on Sep 14, 2012

@author: michel
'''
from OutputFormat import OutputFormat
import StringIO
import os
import tempfile
import FeatureServer.VectorFormats.Formats.SpatialLite

class SpatialLite(OutputFormat):
    def encode(self, result):
        spatiallite = FeatureServer.VectorFormats.Formats.SpatialLite.SpatialLite(layername=self.datasources[0], datasource=self.service.datasources[self.datasources[0]])
        
        try:
            fd, temp_path = tempfile.mkstemp()
            os.close(fd)
            
            connection = spatiallite.encode(result, tmpFile=temp_path)
        
            output = StringIO.StringIO(open(temp_path).read())
        finally:
            os.remove(temp_path)
            
        
        headers = {
            'Accept': '*/*',
            'Content-Disposition' : 'attachment; filename=poidownload.sqlite3',
            'Content-Transfer-Encoding' : 'binary'
        }
        
        return ("application//octet-stream;", output, headers, '')