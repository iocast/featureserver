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

from featureserver.datasource.PostGISHstore import PostGISHstore


class PostGISHstoreTestCase(unittest.TestCase, datasource.Base):
    
    @property
    def table_schema(self):
        return """CREATE TABLE fs_point_hstore (id SERIAL, kvp HSTORE );"""
    @property
    def table_tuples(self):
        return [
                """INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"Carrasquillo", "salary"=>"109000", "street"=>"main street 1986"', ST_GeomFromText('POINT(8.515048 47.461261)', 4326));""",
                """INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"Fewell", "salary"=>"129000"', ST_GeomFromText('POINT(7.581210 47.379493)', 4326));""",
                """INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"Mcmillon", "salary"=>"125000"', ST_GeomFromText('POINT(7.383456 46.983736)', 4326));""",
                """INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"Sykes", "salary"=>"112000", "street"=>"5th avenue"', ST_GeomFromText('POINT(7.877841 46.384567)', 4326));""",
                """INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"Steger", "salary="=>"130000", "street"=>"main street 20"', ST_GeomFromText('POINT(8.811679 46.788513)', 4326));""",
                """INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"Conroy", "salary="=>"120000"', ST_GeomFromText('POINT(8.157992 47.081082)', 4326));""",
                ]
    
    @classmethod
    def setUpClass(cls):
        ''' '''
    
    @classmethod
    def tearDownClass(cls):
        ''' '''
    
    def setUp(self):
        self._connection = psycopg.connect('host=localhost dbname=featureserver user=michel')
        cursor = self._connection.cursor()
        
        cursor.execute(self.table_schema)
        cursor.execute("SELECT AddGeometryColumn ('featureserver', 'public', 'fs_point_hstore', 'geom',4326, 'POINT', 2, false);")
        
        for data in self.table_tuples:
            cursor.execute(data)
        
        
        cursor.close()
        self._connection.commit()
        
        self._fs = Server({
                          'fs_point_hstore' : PostGISHstore('fs_point_hstore', **{
                                               'type': 'PostGISHstore',
                                               'dsn' : 'host=localhost dbname=featureserver user=michel',
                                               'layer' : 'fs_point_hstore',
                                               'fid' : 'id',
                                               'geometry' : 'geom',
                                               'srid' : 4326,
                                               'srid_out' : 4326,
                                               'encoding' : 'utf-8',
                                               'hstore' : 'kvp',
                                               'attribut_cols' : 'kvp',
                                               'additional_cols' : 'hstore(kvp)->\'name\' as "name", hstore(kvp)->\'salary\' as "salary", hstore(kvp)->\'street\' as "street"'
                                               })
                          }, metadata = {'default_output':'WFS', 'default_exception':'WFS'})
    
    def tearDown(self):
        cursor = self._connection.cursor()
        
        cursor.execute("SELECT DropGeometryColumn('featureserver', 'public', 'fs_point_hstore', 'geom');")
        cursor.execute("DROP TABLE fs_point_hstore")
        
        cursor.close()
        
        self._connection.commit()
        self._connection.close()

    
    
    @property
    def data_empty(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> </wfs:FeatureCollection>"""

    @property
    def data_features(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="1"><fs:fs_point_hstore fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:salary>109000</fs:salary><fs:name>Carrasquillo</fs:name><fs:street>main street 1986</fs:street><fs:kvp>"name"=&gt;"Carrasquillo", "salary"=&gt;"109000", "street"=&gt;"main street 1986"</fs:kvp></fs:fs_point_hstore></gml:featureMember><gml:featureMember gml:id="2"><fs:fs_point_hstore fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:salary>129000</fs:salary><fs:name>Fewell</fs:name><fs:street>None</fs:street><fs:kvp>"name"=&gt;"Fewell", "salary"=&gt;"129000"</fs:kvp></fs:fs_point_hstore></gml:featureMember><gml:featureMember gml:id="3"><fs:fs_point_hstore fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:salary>125000</fs:salary><fs:name>Mcmillon</fs:name><fs:street>None</fs:street><fs:kvp>"name"=&gt;"Mcmillon", "salary"=&gt;"125000"</fs:kvp></fs:fs_point_hstore></gml:featureMember><gml:featureMember gml:id="4"><fs:fs_point_hstore fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:salary>112000</fs:salary><fs:name>Sykes</fs:name><fs:street>5th avenue</fs:street><fs:kvp>"name"=&gt;"Sykes", "salary"=&gt;"112000", "street"=&gt;"5th avenue"</fs:kvp></fs:fs_point_hstore></gml:featureMember><gml:featureMember gml:id="5"><fs:fs_point_hstore fid="5"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.811679,46.788513</gml:coordinates></gml:Point><fs:salary>None</fs:salary><fs:name>Steger</fs:name><fs:street>main street 20</fs:street><fs:kvp>"name"=&gt;"Steger", "street"=&gt;"main street 20", "salary="=&gt;"130000"</fs:kvp></fs:fs_point_hstore></gml:featureMember><gml:featureMember gml:id="6"><fs:fs_point_hstore fid="6"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.157992,47.081082</gml:coordinates></gml:Point><fs:salary>None</fs:salary><fs:name>Conroy</fs:name><fs:street>None</fs:street><fs:kvp>"name"=&gt;"Conroy", "salary="=&gt;"120000"</fs:kvp></fs:fs_point_hstore></gml:featureMember></wfs:FeatureCollection>"""
    


class PostGISHstoreWFS110TestCase(PostGISHstoreTestCase):
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point_hstore/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)


class PostGISHstoreWFS200TestCase(PostGISHstoreTestCase):
    ''' '''



def test_suites():
    return [unittest.TestLoader().loadTestsFromTestCase(PostGISHstoreWFS110TestCase), unittest.TestLoader().loadTestsFromTestCase(PostGISHstoreWFS200TestCase)]


