'''
Created on Apr 12, 2011

@author: michel
'''
import unittest
from FeatureServer.FilterEncoding import FilterEncoding as filter
from FeatureServer.Server import Server
from FeatureServer.DataSource.PostGIS import PostGIS

class ObjectIdentifier(unittest.TestCase):
    filters = {'<Filter><ResourceId rid="172251"/></Filter>' : "osm_id = '172251'"}
    
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
    
    def testObjectIdentifiers(self):
        self.datasource = PostGIS('all', **self.params)
        self.server = Server({'all': self.datasource})
        
        for fil, stmt in self.filters.iteritems():
            filterEncoding = filter.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()