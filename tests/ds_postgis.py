import re
import unittest
import datasource

try:
    import psycopg2 as psycopg
except:
    import psycopg

from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request

from featureserver.datasource.PostGIS import PostGIS


class PostGISTestCase(unittest.TestCase, datasource.Base):
    
    table_schema = "CREATE TABLE fs_point (id SERIAL, name TEXT, salary INTEGER );"
    table_tuples = [
                    "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Carrasquillo', 109000, ST_GeomFromText('POINT(8.515048 47.461261)', 4326));",
                    "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Fewell', 129000, ST_GeomFromText('POINT(7.581210 47.379493)', 4326));",
                    "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Mcmillon', 125000, ST_GeomFromText('POINT(7.383456 46.983736)', 4326));",
                    "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Sykes', 112000, ST_GeomFromText('POINT(7.877841 46.384567)', 4326));",
                    "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Steger', 130000, ST_GeomFromText('POINT(8.811679 46.788513)', 4326));",
                    "INSERT INTO fs_point ( name, salary, geom ) VALUES ( 'Conroy', 120000, ST_GeomFromText('POINT(8.157992 47.081082)', 4326));",
                    ]

    @classmethod
    def setUpClass(cls):
        
        
        cls._connection = psycopg.connect('host=localhost dbname=featureserver user=michel')
        cursor = cls._connection.cursor()
        
        cursor.execute(cls.table_schema)
        cursor.execute("SELECT AddGeometryColumn ('featureserver', 'public', 'fs_point', 'geom',4326, 'POINT', 2, false);")
        
        for data in cls.table_tuples:
            cursor.execute(data)
        
        
        cursor.close()
        cls._connection.commit()

        cls._fs = Server({
                         'fs_point' : PostGIS('fs_point', **{
                                              'type': 'PostGIS',
                                              'dsn' : 'host=localhost dbname=featureserver user=michel',
                                              'layer' : 'fs_point',
                                              'fid' : 'id',
                                              'geometry' : 'geom',
                                              'srid' : 4326,
                                              'srid_out' : 4326,
                                              'encoding' : 'utf-8',
                                              'attribut_cols' : 'name',
                                              'additional_cols' : ''
                                              })
                         }, metadata = {'default_output':'WFS', 'default_exception':'WFS'})
    
    @classmethod
    def tearDownClass(cls):
        cursor = cls._connection.cursor()
        
        cursor.execute("SELECT DropGeometryColumn('featureserver', 'public', 'fs_point', 'geom');")
        cursor.execute("DROP TABLE fs_point")        
        
        cursor.close()
        
        cls._connection.commit()
        cls._connection.close()
    
    
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)



    @property
    def data_features(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="1"><fs:fs_point fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:salary>109000</fs:salary><fs:name>Carrasquillo</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:salary>129000</fs:salary><fs:name>Fewell</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="3"><fs:fs_point fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:salary>125000</fs:salary><fs:name>Mcmillon</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="4"><fs:fs_point fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:salary>112000</fs:salary><fs:name>Sykes</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="5"><fs:fs_point fid="5"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.811679,46.788513</gml:coordinates></gml:Point><fs:salary>130000</fs:salary><fs:name>Steger</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="6"><fs:fs_point fid="6"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.157992,47.081082</gml:coordinates></gml:Point><fs:salary>120000</fs:salary><fs:name>Conroy</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>"""

        

def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(PostGISTestCase)

