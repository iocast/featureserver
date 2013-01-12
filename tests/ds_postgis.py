import unittest

from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request

from featureserver.datasource.PostGIS import PostGIS


class PostGISTestCase(unittest.TestCase):
    
    @property
    def fs(self):
        return self._fs
    
    @classmethod
    def setUpClass(cls):
        cls._fs = Server({
                         'fs_point' : PostGIS('fs_point', **{
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
                         })
    
    @classmethod
    def tearDownClass(cls):
        ''' '''
    
    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(response.data.replace("\n", "").replace("\t", ""), self.data_features)




    @property
    def data_features(self):
        return '<?xml version="1.0" ?><wfs:FeatureCollection   xmlns:fs="http://featureserver.org/fs"   xmlns:wfs="http://www.opengis.net/wfs"   xmlns:gml="http://www.opengis.net/gml"   xmlns:ogc="http://www.opengis.net/ogc"   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">        <gml:featureMember gml:id="1"><fs:fs_point fid="1"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.515048,47.461261</gml:coordinates></gml:Point><fs:name>p1</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="2"><fs:fs_point fid="2"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.58121,47.379493</gml:coordinates></gml:Point><fs:name>p2</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="3"><fs:fs_point fid="3"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.383456,46.983736</gml:coordinates></gml:Point><fs:name>p3</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="4"><fs:fs_point fid="4"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">7.877841,46.384567</gml:coordinates></gml:Point><fs:name>p4</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="5"><fs:fs_point fid="5"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.811679,46.788513</gml:coordinates></gml:Point><fs:name>p5</fs:name></fs:fs_point></gml:featureMember><gml:featureMember gml:id="6"><fs:fs_point fid="6"><gml:Point srsName="EPSG:4326"><gml:coordinates decimal="." cs="," ts=" ">8.157992,47.081082</gml:coordinates></gml:Point><fs:name>p6</fs:name></fs:fs_point></gml:featureMember></wfs:FeatureCollection>'
        

def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(PostGISTestCase)

