'''
Created on Apr 12, 2011

@author: michel
'''
import unittest
import FeatureServer.WebFeatureService.FilterEncoding.FilterEncoding as fe
from FeatureServer.Server import Server
from FeatureServer.DataSource.PostGIS import PostGIS

class ComparisonOperatorTestCase(unittest.TestCase):
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
    
    def testComparisonOperators(self):
        filters = {
            "<Filter><PropertyIsEqualTo><ValueReference>highway</ValueReference><Literal>bus_stop</Literal></PropertyIsEqualTo></Filter>" : "\"highway\" = 'bus_stop'",
            "<Filter><PropertyIsNotEqualTo><ValueReference>operator</ValueReference><Literal>UBS</Literal></PropertyIsNotEqualTo></Filter>" : "\"operator\" != 'UBS'",
            "<Filter><PropertyIsLessThan><ValueReference>osm_id</ValueReference><Literal>500000</Literal></PropertyIsLessThan></Filter>" : "\"osm_id\" < '500000'",
            "<Filter><PropertyIsGreaterThan><ValueReference>osm_id</ValueReference><Literal>500000</Literal></PropertyIsGreaterThan></Filter>" : "\"osm_id\" > '500000'",
            "<Filter><PropertyIsLessThanOrEqualTo><ValueReference>osm_id</ValueReference><Literal>500000</Literal></PropertyIsLessThanOrEqualTo></Filter>" : "\"osm_id\" <= '500000'",
            "<Filter><PropertyIsGreaterThanOrEqualTo><ValueReference>osm_id</ValueReference><Literal>500000</Literal></PropertyIsGreaterThanOrEqualTo></Filter>" : "\"osm_id\" >= '500000'",
            "<Filter><PropertyIsBetween><ValueReference>osm_id</ValueReference><LowerBoundary><Literal>1</Literal></LowerBoundary><UpperBoundary><Literal>500000</Literal></UpperBoundary></PropertyIsBetween></Filter>" : "\"osm_id\" BETWEEN '1' AND '500000'",
            '<Filter><PropertyIsLike wildCard="*" singleChar="?" escapeChar="!"><ValueReference>highway</ValueReference><Literal>b?s_sto*</Literal></PropertyIsLike></Filter>' : "\"highway\" LIKE 'b_s_sto%%'"
        }

        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))
    
    def testAndOrCombination(self):
        filters = {
            "<Filter>" +
                "<Or>" +
                    "<And>" +
                        "<PropertyIsEqualTo><ValueReference>operator</ValueReference><Literal>VBZ</Literal></PropertyIsEqualTo>" +
                        "<PropertyIsEqualTo><ValueReference>highway</ValueReference><Literal>bus_stop</Literal></PropertyIsEqualTo>" +
                    "</And>" +
                    "<And>" +
                        "<PropertyIsEqualTo><ValueReference>operator</ValueReference><Literal>BVB</Literal></PropertyIsEqualTo>" +
                        "<PropertyIsEqualTo><ValueReference>highway</ValueReference><Literal>bus_stop</Literal></PropertyIsEqualTo>" +
                    "</And>" +
                "</Or>" + 
            "</Filter>" :
            "((\"operator\" = 'VBZ' AND \"highway\" = 'bus_stop') OR (\"operator\" = 'BVB' AND \"highway\" = 'bus_stop'))",
            "<Filter>" +
               "<And>" +
                  "<PropertyIsEqualTo>" +
                     "<PropertyName>shop</PropertyName>" +
                     "<Literal>supermarket</Literal>" +
                  "</PropertyIsEqualTo>" +
                  "<PropertyIsLike wildCard=\"*\" singleChar=\".\" escapeChar=\"!\">" +
                     "<PropertyName>name</PropertyName>" +
                     "<Literal>.enner*</Literal>" +
                  "</PropertyIsLike>" +
               "</And>" +
            "</Filter>" :
            "(\"shop\" = 'supermarket' AND \"name\" LIKE '_enner%%')"
        }

        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))
       

class ComparisonOperatorTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self,map(ComparisonOperatorTestCase,
                                                     ("testComparisonOperators",
                                                      "testAndOrCombination")))

def suite(): 
    suite = unittest.TestSuite()
    suite.addTest(ComparisonOperatorTestCase('testComparisonOperators'))
    suite.addTest(ComparisonOperatorTestCase('testAndOrCombination'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()