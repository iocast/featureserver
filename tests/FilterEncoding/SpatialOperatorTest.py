'''
Created on Apr 12, 2011

@author: michel
'''
import unittest
import FeatureServer.FilterEncoding.FilterEncoding as fe
from FeatureServer.Server import Server
from FeatureServer.DataSource.PostGIS import PostGIS

class SpatialOperatorTestCase(unittest.TestCase):
    datasource = None
    server = None
    params = {'type': 'PostGIS',
              'title': 'All',
              'abstract': 'All',
              'dsn' : 'host=localhost dbname=osm_pg_ch user=gisuser password=gisuser',
              'layer' : 'planet_osm_point',
              'fid': 'osm_id',
              'geometry': 'way',
              'srid' : '4326',
              'attribute_cols' : 'name,amenity,operator,bridge,highway,power,place,route',
              'bbox' : '5.95459 45.75986 10.52490 47.83528'}
    
    def setUp(self):
        self.datasource = PostGIS('all', **self.params)
        self.server = Server({'all': self.datasource})
    def tearDown(self):
        self.datasource = None
        self.server = None
    
    def testEquals(self):
        filters = {
            "<Filter>" +
                "<Equals>" + 
                    "<ValueReference>way</ValueReference>" +
                    "<Literal>" +
                        "<gml:Point srsName=\"EPSG:4326\">" +
                            "<gml:coordinates>5.9656087,46.144381600000003</gml:coordinates>" +
                        "</gml:Point>" +
                    "</Literal>" +
                "</Equals>" +
            "</Filter>" :
            "ST_Equals(way, ST_GeomFromGML('<gml:Point xmlns:gml=\"http://www.opengis.net/gml\" xmlns:regexp=\"http://exslt.org/regular-expressions\" srsName=\"EPSG:4326\"><gml:coordinates>5.9656087,46.144381600000003</gml:coordinates></gml:Point>'))"
        }
    
        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))
            
    def testBBOX(self):
        filters = {
            "<Filter>" +
                "<BBOX>" + 
                    "<ValueReference>way</ValueReference>" +
                    "<gml:Envelope xmlns:gml=\"http://www.opengis.net/gml\" srsName=\"asdf:EPSG:4326\">" +
                        "<gml:lowerCorner>5.95459 45.75986</gml:lowerCorner>" +
                        "<gml:upperCorner>10.52490 47.83528</gml:upperCorner>" + 
                    "</gml:Envelope>" +
                "</BBOX>" +
            "</Filter>" :
            "NOT ST_Disjoint(way, ST_MakeEnvelope(5.95459,45.75986,10.52490,47.83528, 4326))"
        }
        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))

class SpatialOperatorTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self,map(SpatialOperatorTestCase,
                                                     ("testEquals",
                                                      "testBBOX")))

def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(SpatialOperatorTestCase('testEquals'))
    suite.addTest(SpatialOperatorTestCase('testBBOX'))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(defaultTest='suite')
    
    
    