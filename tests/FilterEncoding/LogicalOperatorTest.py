'''
Created on Apr 12, 2011

@author: michel
'''
import unittest
from FeatureServer.FilterEncoding import FilterEncoding as fe
from FeatureServer.Server import Server
from FeatureServer.DataSource.PostGIS import PostGIS

class LogicalOperatorTestCase(unittest.TestCase):
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
    
    def testAndOperator(self):
        filters = {
            "<Filter>" +
                "<And>" + 
                    "<PropertyIsEqualTo>" +
                        "<ValueReference>highway</ValueReference>" +
                        "<Literal>bus_stop</Literal>" +
                    "</PropertyIsEqualTo>" +
                    "<PropertyIsEqualTo>" +
                        "<ValueReference>operator</ValueReference>" +
                        "<Literal>VBZ</Literal>" +
                    "</PropertyIsEqualTo>" +
                "</And>" +
            "</Filter>" :
            "(highway = 'bus_stop' AND operator = 'VBZ')"
        }

        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))

    def testOrOperator(self):
        filters = { 
            "<Filter>" +
                "<And>" + 
                    "<Or>" +
                        "<PropertyIsEqualTo>" +
                            "<ValueReference>FIELD1</ValueReference>" +
                            "<Literal>10</Literal>" +
                        "</PropertyIsEqualTo>" +
                        "<PropertyIsEqualTo>" +
                            "<ValueReference>FIELD1</ValueReference>" +
                            "<Literal>20</Literal>" +
                        "</PropertyIsEqualTo>" +
                    "</Or>" +
                    "<PropertyIsEqualTo>" +
                        "<ValueReference>STATUS</ValueReference>" +
                        "<Literal>VALID</Literal>" +
                    "</PropertyIsEqualTo>" +
                "</And>" +
            "</Filter>" :
            "((FIELD1 = '10' OR FIELD1 = '20') AND STATUS = 'VALID')"
        }

        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))

    def testNotOperator(self):
        filters = { 
            "<Filter>" +
                "<And>" + 
                    "<PropertyIsEqualTo>" +
                        "<ValueReference>highway</ValueReference>" +
                        "<Literal>bus_stop</Literal>" +
                    "</PropertyIsEqualTo>" +
                    "<Not>" +
                        "<PropertyIsEqualTo>" +
                            "<ValueReference>operator</ValueReference>" +
                            "<Literal>VBZ</Literal>" +
                        "</PropertyIsEqualTo>" +
                    "</Not>" +
                "</And>" +
            "</Filter>" :
            "(highway = 'bus_stop' AND NOT operator = 'VBZ')",
            "<Filter>" +
                "<And>" + 
                    "<PropertyIsEqualTo>" +
                        "<ValueReference>highway</ValueReference>" +
                        "<Literal>bus_stop</Literal>" +
                    "</PropertyIsEqualTo>" +
                    "<Not>" +
                        "<PropertyIsEqualTo>" +
                            "<ValueReference>operator</ValueReference>" +
                            "<Literal>VBZ</Literal>" +
                        "</PropertyIsEqualTo>" +
                    "</Not>" +
                    "<Not>" +
                        "<PropertyIsEqualTo>" +
                            "<ValueReference>operator</ValueReference>" +
                            "<Literal>BVB</Literal>" +
                        "</PropertyIsEqualTo>" +
                    "</Not>" +
                "</And>" +
            "</Filter>" :
            "(highway = 'bus_stop' AND NOT operator = 'VBZ' AND NOT operator = 'BVB')"
        }

        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))

class LogicalOperatorTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self,map(LogicalOperatorTestCase,
                                                     ("testAndOperator",
                                                      "testOrOperator",
                                                      "testNotOperator")))

def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(LogicalOperatorTestCase('testAndOperator'))
    suite.addTest(LogicalOperatorTestCase('testOrOperator'))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(defaultTest='suite')