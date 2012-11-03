'''
Created on Oct 16, 2011

@author: michel
'''
import unittest
import FeatureServer.FilterEncoding.FilterEncoding as fe
from FeatureServer.Server import Server
from FeatureServer.DataSource.PostGIS import PostGIS
from FeatureServer.Transaction.Transaction import Transaction
    
class TransactionTest(unittest.TestCase):
    datasource = None
    server = None
    params = {'type': 'PostGIS',
              'title': 'All',
              'abstract': 'All',
              'dsn' : 'host=localhost dbname=osm_test user=postgres password=4mrafk3',
              'layer' : 'osm_point',
              'fid': 'osm_id',
              'geometry': 'way',
              'version' : 'osm_version',
              'srid' : '4326',
              'srid_out' : '4326',
              'attribute_cols' : 'name,amenity,operator,bridge,highway,power,place,route',
              'bbox' : '5.95459 45.75986 10.52490 47.83528',
              'ele' : 'ele',
              'geometry_type' : 'Point'}

    def setUp(self):
        self.datasource = PostGIS('all', **self.params)
        self.server = Server({'all': self.datasource})

    def tearDown(self):
        self.datasource = None
        self.server = None

    def testInsert(self):
        xml = """<?xml version="1.0"?>
<wfs:Transaction
       version="1.1.0"
       service="WFS"
       xmlns="http://featureserver.org/fs"
       xmlns:gml="http://www.opengis.net/gml"
       xmlns:ogc="http://www.opengis.net/ogc"
       xmlns:wfs="http://www.opengis.net/wfs"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">
    <wfs:Insert idgen="GenerateNew">
        <osm_point gml:id="1">
            <way>
                <gml:Point srsName="EPSG:4326">
                    <gml:coordinates decimal="." cs="," ts=" ">8.53438799881,47.3187879949</gml:coordinates>
                </gml:Point>
            </way>
            <name>honky1</name>
            <operator>ABC</operator>
            <highway>bus_stop</highway>
        </osm_point>
        
        <osm_point gml:id="2">
            <way>
                <gml:Point srsName="EPSG:4326">
                    <gml:coordinates decimal="." cs="," ts=" ">8.52892699881,47.3221139949</gml:coordinates>
                </gml:Point>
            </way>
            <highway>bus_stop</highway>
        </osm_point>
        
    </wfs:Insert>
</wfs:Transaction>    
            """
        solution = [" INSERT INTO osm_point ( \"way\" , \"name\" , \"operator\" , \"highway\" ) VALUES ( ST_GeomFromGML('<gml:Point xmlns:gml=\"http://www.opengis.net/gml\" xmlns=\"http://featureserver.org/fs\" xmlns:ogc=\"http://www.opengis.net/ogc\" xmlns:wfs=\"http://www.opengis.net/wfs\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" srsName=\"EPSG:4326\"> <gml:coordinates decimal=\".\" cs=\",\" ts=\" \">8.53438799881,47.3187879949</gml:coordinates> </gml:Point> ') , 'honky1' , 'ABC' , 'bus_stop' ); ",
                    " INSERT INTO osm_point ( \"way\" , \"highway\" ) VALUES ( ST_GeomFromGML('<gml:Point xmlns:gml=\"http://www.opengis.net/gml\" xmlns=\"http://featureserver.org/fs\" xmlns:ogc=\"http://www.opengis.net/ogc\" xmlns:wfs=\"http://www.opengis.net/wfs\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" srsName=\"EPSG:4326\"> <gml:coordinates decimal=\".\" cs=\",\" ts=\" \">8.53438799881,47.3187879949</gml:coordinates> </gml:Point> ') , 'bus_stop' ); "]
        result = []
        
        transaction = Transaction()
        transaction.parse(xml)
        transactions = transaction.getActions()
                                                
        for transaction in transactions:
            result.append(transaction.getStatement(self.datasource))
        
        self.assertItemsEqual(solution, result)
        
    def testUpdate(self):
        xml = """<?xml version="1.0"?>
<wfs:Transaction
       version="1.1.0"
       service="WFS"
       xmlns="http://featureserver.org/fs"
       xmlns:gml="http://www.opengis.net/gml"
       xmlns:ogc="http://www.opengis.net/ogc"
       xmlns:wfs="http://www.opengis.net/wfs"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">
    <wfs:Update typeName="test_point" xmlns:feature="http://opengeo.org">
        <wfs:Property>
            <wfs:Name>way</wfs:Name>
            <wfs:Value>
                <gml:Point srsName="EPSG:4326">
                    <gml:coordinates decimal="." cs="," ts=" ">8.53438799881,47.3187879949</gml:coordinates>
                </gml:Point>
            </wfs:Value>
        </wfs:Property>
        <wfs:Property>
            <wfs:Name>Description</wfs:Name>
            <wfs:Value>abc</wfs:Value>
        </wfs:Property>
        <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:FeatureId fid="1"/>
        </ogc:Filter>
    </wfs:Update>
    <wfs:Update typeName="test_point" xmlns:feature="http://opengeo.org">
        <wfs:Property>
            <wfs:Name>way</wfs:Name>
            <wfs:Value>
                <gml:Point srsName="EPSG:4326">
                    <gml:coordinates decimal="." cs="," ts=" ">8.53438799881,47.3187879949</gml:coordinates>
                </gml:Point>
            </wfs:Value>
        </wfs:Property>
        <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:FeatureId fid="2"/>
        </ogc:Filter>
    </wfs:Update>
</wfs:Transaction> """         
        solution = [" UPDATE osm_point SET \"way\" = ST_GeomFromGML('<gml:Point xmlns:gml=\"http://www.opengis.net/gml\" xmlns:feature=\"http://opengeo.org\" xmlns=\"http://featureserver.org/fs\" xmlns:ogc=\"http://www.opengis.net/ogc\" xmlns:wfs=\"http://www.opengis.net/wfs\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" srsName=\"EPSG:4326\"> <gml:coordinates decimal=\".\" cs=\",\" ts=\" \">8.53438799881,47.3187879949</gml:coordinates> </gml:Point> ') , \"Description\" = 'abc' WHERE \"osm_id\" = '1'; ",
                    " UPDATE osm_point SET \"way\" = ST_GeomFromGML('<gml:Point xmlns:gml=\"http://www.opengis.net/gml\" xmlns:feature=\"http://opengeo.org\" xmlns=\"http://featureserver.org/fs\" xmlns:ogc=\"http://www.opengis.net/ogc\" xmlns:wfs=\"http://www.opengis.net/wfs\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" srsName=\"EPSG:4326\"> <gml:coordinates decimal=\".\" cs=\",\" ts=\" \">8.53438799881,47.3187879949</gml:coordinates> </gml:Point> ') WHERE \"osm_id\" = '2'; "]
        result = []

        transaction = Transaction()
        transaction.parse(xml)
        transactions = transaction.getActions()
                                                
        for transaction in transactions:
            result.append(transaction.getStatement(self.datasource))
        
        self.assertItemsEqual(solution, result)
            
    def testDelete(self):
        xml = """<?xml version="1.0"?>
<wfs:Transaction
       version="1.1.0"
       service="WFS"
       xmlns="http://featureserver.org/fs"
       xmlns:gml="http://www.opengis.net/gml"
       xmlns:ogc="http://www.opengis.net/ogc"
       xmlns:wfs="http://www.opengis.net/wfs"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">
    <wfs:Delete typeName="test_point" xmlns:feature="http://opengeo.org">
        <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:FeatureId fid="1"/>
        </ogc:Filter>
    </wfs:Delete>
    <wfs:Delete typeName="test_point" xmlns:feature="http://opengeo.org">
        <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:FeatureId fid="2"/>
        </ogc:Filter>
    </wfs:Delete>
</wfs:Transaction> """
        solution = [" DELETE FROM osm_point WHERE \"osm_id\" = '1'; ", " DELETE FROM osm_point WHERE \"osm_id\" = '2'; "]
        result = []

        transaction = Transaction()
        transaction.parse(xml)
        transactions = transaction.getActions()
                                                
        for transaction in transactions:
            result.append(transaction.getStatement(self.datasource))
        
        self.assertItemsEqual(solution, result)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()