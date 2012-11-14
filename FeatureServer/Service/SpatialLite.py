'''
Created on Sep 14, 2012

@author: michel
'''
from FeatureServer.Service.Service import Service
import StringIO
import os
import tempfile
import VectorFormats.Formats.SpatialLite

class SpatialLite(Service):
    def encode(self, result):
        spatiallite = vectorformats.Formats.SpatialLite.SpatialLite(layername=self.datasources[0], datasource=self.service.datasources[self.datasources[0]])
        
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