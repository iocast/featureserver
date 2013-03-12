import datasource
import unittest
import re

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from featureserver.datasource.GeoAlchemy import GeoAlchemy
from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request


from .model_geoalchemy import FSPoint, metadata, session

class GeoAlchemyTestCase(unittest.TestCase, datasource.Base):
    
    @classmethod
    def setUpClass(cls):
        ''' '''
    
    @classmethod
    def tearDownClass(cls):
        ''' '''
    
    def setUp(self):
        metadata.create_all()
        
        ds = GeoAlchemy('fs_point', **{
                        'type': 'GeoAlchemy',
                        'model': 'tests.model_geoalchemy',
                        'dburi': 'sqlite://',
                        'cls': 'FSPoint',
                        'fid': 'id',
                        'geometry': 'geom',
                        'session' : session
                        })
        self._fs = Server({'fs_point': ds})
    
    def tearDown(self):
        ''' '''
    #metadata.drop_all()
    

    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(re.sub(' +', ' ', response.data.replace("\n", "").replace("\t", "")), "")

        #def test_dispatch_request(self):
#self.assertEqual(self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point", params = {'format':'geojson', 'version':'1.1.0'})), ('text/plain', '{"crs": null, "type": "FeatureCollection", "features": []}'))





def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(GeoAlchemyTestCase)