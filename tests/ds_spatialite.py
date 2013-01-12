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
    
    @property
    def table_schema(self):
        return 'CREATE TABLE fs_point (' \
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                    'name TEXT' \
                ');'
    @property
    def table_tuples(self):
        return [
                "INSERT INTO fs_point ( name, geom ) VALUES ( 'p1', ST_GeomFromText('POINT(8.515048 47.461261)', 4326));",
                "INSERT INTO fs_point ( name, geom ) VALUES ( 'p2', ST_GeomFromText('POINT(7.581210 47.379493)', 4326));",
                "INSERT INTO fs_point ( name, geom ) VALUES ( 'p3', ST_GeomFromText('POINT(7.383456 46.983736)', 4326));",
                "INSERT INTO fs_point ( name, geom ) VALUES ( 'p4', ST_GeomFromText('POINT(7.877841 46.384567)', 4326));",
                "INSERT INTO fs_point ( name, geom ) VALUES ( 'p5', ST_GeomFromText('POINT(8.811679 46.788513)', 4326));",
                "INSERT INTO fs_point ( name, geom ) VALUES ( 'p6', ST_GeomFromText('POINT(8.157992 47.081082)', 4326));",
        ]

    
    def setUp(self):
        self._fs = Server({  'fs_point' : SpatiaLite('fs_point', **{
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
        self.fs.datasources['fs_point'].begin()
        self.fs.datasources['fs_point'].connection.cursor().execute("SELECT InitSpatialMetadata()")
        self.fs.datasources['fs_point'].connection.cursor().execute(self.table_schema)
        self.fs.datasources['fs_point'].connection.cursor().execute("SELECT AddGeometryColumn('fs_point', 'geom', 4326, 'POINT', 'XY')")
        for stmt in self.table_tuples:
            self.fs.datasources['fs_point'].connection.cursor().execute(stmt)
            
    def tearDown(self):
        ''' '''
    
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(response.data.replace("\n", "").replace("\t", ""), self.data_features)

    def test_keyword_by_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/2.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(response.data.replace("\n", "").replace("\t", ""), self.data_feature_two)



    
    
    @property
    def data_features(self):
        return '<?xml version="1.0" ?><wfs:FeatureCollection   xmlns:fs="http://featureserver.org/fs"   xmlns:wfs="http://www.opengis.net/wfs"   xmlns:gml="http://www.opengis.net/gml"   xmlns:ogc="http://www.opengis.net/ogc"   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">        <gml:featureMember gml:id="1"><fs:fs_point fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:name>p1</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:name>p2</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="3"><fs:fs_point fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:name>p3</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="4"><fs:fs_point fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:name>p4</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="5"><fs:fs_point fid="5"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.811679,46.788513</gml:coordinates></gml:Point><fs:name>p5</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="6"><fs:fs_point fid="6"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.157992,47.081082</gml:coordinates></gml:Point><fs:name>p6</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>'

    @property
    def data_feature_two(self):
        return '<?xml version="1.0" ?><wfs:FeatureCollection   xmlns:fs="http://featureserver.org/fs"   xmlns:wfs="http://www.opengis.net/wfs"   xmlns:gml="http://www.opengis.net/gml"   xmlns:ogc="http://www.opengis.net/ogc"   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">        <gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:name>p2</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>'


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(SpatiaLiteTestCase)

