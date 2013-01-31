import datasource
import unittest

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from .model_geoalchemy import FSPoint, metadata

from featureserver.datasource.GeoAlchemy import GeoAlchemy
from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request


class GeoAlchemyTestCase(unittest.TestCase, datasource.Base):
    
    @classmethod
    def setUpClass(cls):
        #metadata.create_all()
        
        ds = GeoAlchemy('fs_point', **{
                        'type': 'GeoAlchemy',
                        'model': 'tests.model_geoalchemy',
                        'dburi': 'sqlite:///:memory:',
                        'cls': 'FSPoint',
                        'fid': 'id',
                        'geometry': 'geom'
                        })
        cls._fs = Server({'fs_point': ds})
    
    @classmethod
    def tearDownClass(cls):
        metadata.drop_all()
    

    def test_keyword_features(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point/features.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(response.data.replace("\n", "").replace("\t", ""), "")

    def test_dispatch_request(self):
        self.assertEqual(self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/fs_point", params = {'format':'geojson', 'version':'1.1.0'})), ('text/plain', '{"crs": null, "type": "FeatureCollection", "features": []}'))





def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(GeoAlchemyTestCase)