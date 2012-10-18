'''
Created on May 18, 2011

@author: michel
'''
import unittest
from FeatureServer.Service.SHP import SHP
from FeatureServer.Server import Server
from FeatureServer.DataSource.PostGIS import PostGIS

class ShapeFileTestCase(unittest.TestCase):
    datasource = None
    server = None
    config = {'type': 'PostGIS',
              'title': 'All',
              'abstract': 'All',
              'dsn' : 'host=localhost dbname=test_gis_ch user=gisuser password=gisuser',
              'layer' : 'planet_osm_polygon',
              'fid': 'osm_id',
              'geometry': 'way',
              'srid' : '4326',
              'attribute_cols' : 'boundary,name,landuse',
              'bbox' : '5.95459 45.75986 10.52490 47.83528'}
    service = None

    def setUp(self):
        self.datasource = PostGIS('all', **self.config)
        self.server = Server({'all': self.datasource})
        self.service = SHP(self.server)
        
    def tearDown(self):
        self.service = None
        self.datasource = None
        self.server = None
    
    def testShapeFile(self):
        params = {'filter': '<Filter><Or>' +
                        '<PropertyIsEqualTo><ValueReference>landuse</ValueReference><Literal>vineyard</Literal></PropertyIsEqualTo>' +
                        '<PropertyIsEqualTo><ValueReference>boundary</ValueReference><Literal>administrative</Literal></PropertyIsEqualTo>' +
                    '</Or></Filter>',
                'typename': 'all',
                'version': '1.0.0',
                'request': 'GetFeature', 
                'service': 'WFS'
        }
        path_info = '/'
        host = 'http://localhost:8080'
        post_data = None
        request_method = 'GET'
        
        response = []
        
        self.service.parse(params, path_info, host, post_data, request_method)
        self.datasource.begin()
        for action in self.service.actions:
            method = getattr(self.datasource, action.method)
            result = method(action)
            response += result 
        self.datasource.commit()

        mime, data, headers = self.service.encode(response)
        #data = data.encode("utf-8") 
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()        