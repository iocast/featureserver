import unittest

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from .model_geoalchemy import Road, metadata

from featureserver.datasource.GeoAlchemy import GeoAlchemy
from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request


class GeoAlchemyTestCase(unittest.TestCase):
    
    @property
    def fs(self):
        return self._fs
    
    @classmethod
    def setUpClass(cls):
        metadata.create_all()
        
        ds = GeoAlchemy('roads', **{
                        'type': 'GeoAlchemy',
                        'model': 'tests.model_geoalchemy',
                        'dburi': 'postgres://michel@localhost/featureserver',
                        'cls': 'Road',
                        'fid': 'id',
                        'geometry': 'geom'
                        })
        cls._fs = Server({'roads': ds})
    
    @classmethod
    def tearDownClass(cls):
        metadata.drop_all()
    
    
    def test_dispatch_request(self):
        self.assertEqual(self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/roads", params = {'format':'geojson', 'version':'1.1.0'})), ('text/plain', '{"crs": null, "type": "FeatureCollection", "features": []}'))


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(GeoAlchemyTestCase)