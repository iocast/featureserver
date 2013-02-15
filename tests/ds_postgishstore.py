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
        return """CREATE TABLE fs_point_hstore (id SERIAL, dummy TEXT, kvp HSTORE );"""
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
                                               'attribute_cols' : 'kvp',
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

    @property
    def data_feature_two(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="2"><fs:fs_point_hstore fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:salary>129000</fs:salary><fs:name>Fewell</fs:name><fs:street>None</fs:street><fs:kvp>"name"=&gt;"Fewell", "salary"=&gt;"129000"</fs:kvp></fs:fs_point_hstore></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_features_bbox(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="3"><fs:fs_point_hstore fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:salary>125000</fs:salary><fs:name>Mcmillon</fs:name><fs:street>None</fs:street><fs:kvp>"name"=&gt;"Mcmillon", "salary"=&gt;"125000"</fs:kvp></fs:fs_point_hstore></gml:featureMember><gml:featureMember gml:id="4"><fs:fs_point_hstore fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:salary>112000</fs:salary><fs:name>Sykes</fs:name><fs:street>5th avenue</fs:street><fs:kvp>"name"=&gt;"Sykes", "salary"=&gt;"112000", "street"=&gt;"5th avenue"</fs:kvp></fs:fs_point_hstore></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_insert_single_response(self):
        return """<?xml version="1.0" encoding="UTF-8"?> <wfs:TransactionResponse version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:og="http://opengeo.org" xmlns:ogc="http://www.opengis.net/ogc" xmlns:tiger="http://www.census.gov" xmlns:cite="http://www.opengeospatial.net/cite" xmlns:nurc="http://www.nurc.nato.int" xmlns:sde="http://geoserver.sf.net" xmlns:analytics="http://opengeo.org/analytics" xmlns:wfs="http://www.opengis.net/wfs" xmlns:topp="http://www.openplans.org/topp" xmlns:it.geosolutions="http://www.geo-solutions.it" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sf="http://www.openplans.org/spearfish" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:za="http://opengeo.org/za" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:tike="http://opengeo.org/#tike"> <wfs:TransactionSummary> <wfs:totalInserted>1</wfs:totalInserted> <wfs:totalUpdated>0</wfs:totalUpdated> <wfs:totalDeleted>0</wfs:totalDeleted> <wfs:totalReplaced>0</wfs:totalReplaced> </wfs:TransactionSummary> <wfs:TransactionResults/> <wfs:InsertResults><wfs:Feature handle=""><ogc:ResourceId fid="7"/></wfs:Feature></wfs:InsertResults><wfs:UpdateResults></wfs:UpdateResults><wfs:ReplaceResults></wfs:ReplaceResults><wfs:DeleteResults></wfs:DeleteResults><wfs:TransactionResult> <wfs:Status> <wfs:SUCCESS/></wfs:Status> </wfs:TransactionResult></wfs:TransactionResponse>"""
    @property
    def data_insert_single_feature(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="7"><fs:fs_point_hstore fid="7"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.65237703581,47.2491447055</gml:coordinates></gml:Point><fs:salary>None</fs:salary><fs:name>None</fs:name><fs:street>None</fs:street><fs:kvp>None</fs:kvp></fs:fs_point_hstore></gml:featureMember></wfs:FeatureCollection>"""

    @property
    def data_update_single_response(self):
        return """<?xml version="1.0" encoding="UTF-8"?> <wfs:TransactionResponse version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd" xmlns:og="http://opengeo.org" xmlns:ogc="http://www.opengis.net/ogc" xmlns:tiger="http://www.census.gov" xmlns:cite="http://www.opengeospatial.net/cite" xmlns:nurc="http://www.nurc.nato.int" xmlns:sde="http://geoserver.sf.net" xmlns:analytics="http://opengeo.org/analytics" xmlns:wfs="http://www.opengis.net/wfs" xmlns:topp="http://www.openplans.org/topp" xmlns:it.geosolutions="http://www.geo-solutions.it" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sf="http://www.openplans.org/spearfish" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:za="http://opengeo.org/za" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:tike="http://opengeo.org/#tike"> <wfs:TransactionSummary> <wfs:totalInserted>0</wfs:totalInserted> <wfs:totalUpdated>1</wfs:totalUpdated> <wfs:totalDeleted>0</wfs:totalDeleted> <wfs:totalReplaced>0</wfs:totalReplaced> </wfs:TransactionSummary> <wfs:TransactionResults/> <wfs:InsertResults></wfs:InsertResults><wfs:UpdateResults><wfs:Feature handle=""><ogc:ResourceId fid="1"/></wfs:Feature></wfs:UpdateResults><wfs:ReplaceResults></wfs:ReplaceResults><wfs:DeleteResults></wfs:DeleteResults><wfs:TransactionResult> <wfs:Status> <wfs:SUCCESS/></wfs:Status> </wfs:TransactionResult></wfs:TransactionResponse>"""
    @property
    def data_update_single_feature(self):
        return """<?xml version="1.0" ?><wfs:FeatureCollection xmlns:fs="http://featureserver.org/fs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd"> <gml:featureMember gml:id="1"><fs:fs_point_hstore fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:salary>90900</fs:salary><fs:name>Alfredo</fs:name><fs:street>main street 1986</fs:street><fs:kvp>"name"=&gt;"Alfredo", "salary"=&gt;"90900", "street"=&gt;"main street 1986"</fs:kvp></fs:fs_point_hstore></gml:featureMember></wfs:FeatureCollection>"""




class PostGISHstoreWFS110TestCase(PostGISHstoreTestCase):
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point_hstore/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)

    def test_keyword_by_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point_hstore/2.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)

    def test_get_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs", params = {'version':'1.1.0', 'request':'GetFeature', 'typename':'fs_point_hstore'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)

    def test_get_bbox(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {'service':'WFS','version':'1.1.0', 'request':'GetFeature', 'typename':'fs_point_hstore', 'bbox':'7.0,46.0,8.0,47.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features_bbox)

    def test_post_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="fs_point_hstore" srsName="EPSG:4326" /></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_features)

    def test_post_by_gml_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="fs_point_hstore" srsName="EPSG:4326" /><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:GmlObjectId xmlns:gml="http://www.opengis.net/gml" gml:id="2"/></ogc:Filter></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)
    
    def test_post_by_feat_id(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "", params = {}, request_method = "POST", post_data = '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Query typeName="fs_point_hstore" srsName="EPSG:4326" /><ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:FeatureId fid="2"/></ogc:Filter></wfs:GetFeature>'))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_feature_two)

    def test_post_insert_single(self):
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><wfs:Insert><fs_point_hstore xmlns:feature="http://example.com/featureserver"><geom><gml:Point xmlns:gml="http://www.opengis.net/gml" srsName="EPSG:4326"><gml:pos>8.65237703580643 47.2491447055323</gml:pos></gml:Point></geom></fs_point_hstore></wfs:Insert></wfs:Transaction>')
        transactions = self.ds_process('fs_point_hstore', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_insert_single_response)
        
        # test if feature was inserted into database by querying by its id
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point_hstore/7.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_insert_single_feature)
    
    def test_post_update_single(self):
        # update feature 1
        request = Request(base_path = "", path_info = "", params = {}, request_method = "PUT", post_data = '<wfs:Transaction xmlns:wfs="http://www.opengis.net/wfs" service="WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"><wfs:Update typeName="fs_point_hstore"><wfs:Property><wfs:Name>kvp</wfs:Name><wfs:Value>kvp || ("name" =&gt; "Alfredo")</wfs:Value></wfs:Property><wfs:Property><wfs:Name>kvp</wfs:Name><wfs:Value>kvp || ("salary" =&gt; "90900")</wfs:Value></wfs:Property><ogc:Filter><ogc:FeatureId fid="1"/></ogc:Filter></wfs:Update></wfs:Transaction>')
        transactions = self.ds_process('fs_point_hstore', request)
        
        # test WFS resonse summary
        response = self.fs.respond_service(response=transactions, service=request.service)
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_update_single_response)
        
        # test if feature was inserted into database by querying by its id
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point_hstore/1.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), self.data_update_single_feature)




class PostGISHstoreWFS200TestCase(PostGISHstoreTestCase):
    ''' '''



def test_suites():
    return [unittest.TestLoader().loadTestsFromTestCase(PostGISHstoreWFS110TestCase), unittest.TestLoader().loadTestsFromTestCase(PostGISHstoreWFS200TestCase)]


