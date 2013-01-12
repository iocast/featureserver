import unittest

from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request


class WFSTestCase(unittest.TestCase):
    
    @property
    def fs(self):
        return self._fs
    
    @classmethod
    def setUpClass(cls):
        cls._fs = Server({})
    
    @classmethod
    def tearDownClass(cls):
        ''' '''
    
    def test_keyword_capabilities(self):
        wfs = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/capabilities.wfs", params = {'version':'1.1.0'}))
        print wfs
        self.assertEqual(wfs, ('text/plain', '{"crs": null, "type": "FeatureCollection", "features": []}'))


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(WFSTestCase)