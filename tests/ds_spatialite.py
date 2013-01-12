import unittest
import sqlite3

from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request

from featureserver.datasource.SpatiaLite import SpatiaLite


class SpatiaLiteTestCase(unittest.TestCase):
    
    @property
    def fs(self):
        return self._fs
    
    @classmethod
    def table_schema(self):
        return 'CREATE TABLE fs_point (' \
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                    'name TEXT' \
                ');'
    
    
    @classmethod
    def setUpClass(cls):
        cls._fs = Server({  'fs_point' : SpatiaLite('fs_point', **{
                                                    'file' : ':memory:',
                                                    'layer' : 'fs_point',
                                                    'fid' : 'id',
                                                    'geometry' : 'geom',
                                                    'srid' : 4326,
                                                    'srid_out' : 4326,
                                                    'encoding' : 'utf-8',
                                                    'attribut_cols' : 'name',
                                                    'additional_cols' : ''
                                                    })
                         })
        cls._fs.datasources['fs_point'].begin()
        cls._fs.datasources['fs_point'].connection.cursor().execute("SELECT InitSpatialMetadata()")
        cls._fs.datasources['fs_point'].connection.cursor().execute(cls.table_schema())
        cls._fs.datasources['fs_point'].connection.cursor().execute("SELECT AddGeometryColumn('fs_point', 'geom', 4326, 'POINT', 'XY')")
        cls._fs.datasources['fs_point'].connection.cursor().execute("INSERT INTO fs_point ( name, geom ) VALUES ( 'p1', GeomFromText('POINT(8.515048 47.461261)', 4326));")
            
    @classmethod
    def tearDownClass(cls):
        ''' '''
    
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(response.data.replace("\n", "").replace("\t", ""), self.data_features)
    
    
    
    @property
    def data_features(self):
        return '<?xml version="1.0" ?><wfs:FeatureCollection   xmlns:fs="http://featureserver.org/fs"   xmlns:wfs="http://www.opengis.net/wfs"   xmlns:gml="http://www.opengis.net/gml"   xmlns:ogc="http://www.opengis.net/ogc"   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">        <gml:featureMember gml:id="1"><fs:fs_point fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:name>p1</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>'


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(SpatiaLiteTestCase)

