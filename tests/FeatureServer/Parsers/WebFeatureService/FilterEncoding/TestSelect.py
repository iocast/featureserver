import unittest

from FeatureServer.DataSource.SpatialLite import SpatialLite

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.datasource = SpatialLite("fs_test", "")
        self.xml = ""

    
    
<?xml version="1.0" ?>
    <GetFeature
version="1.1.0"
service="WFS"
handle="Example Query"
xmlns="http://www.opengis.net/wfs" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" xmlns:myns="http://www.someserver.com/myns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs ../wfs/1.1.0/WFS.xsd"> <Query typeName="myns:ROADS">
    <wfs:PropertyName>myns:path</wfs:PropertyName>
    <wfs:PropertyName>myns:lanes</wfs:PropertyName>
    <wfs:PropertyName>myns:surfaceType</wfs:PropertyName>
    <ogc:Filter>
        <ogc:Within>
            <ogc:PropertyName>myns:path</ogc:PropertyName>
            <gml:Envelope srsName="EPSG:63266405">
                <gml:lowerCorner>50 40</gml:lowerCorner>
                <gml:upperCorner>100 60</gml:upperCorner>
            </gml:Envelope>
        </ogc:Within>
    </ogc:Filter>
        </Query>
        <Query typeName="myns:Rails">
            <wfs:PropertyName>myns:track</wfs:PropertyName>
            <wfs:PropertyName>myns:gauge</wfs:PropertyName>
            <ogc:Filter>
                <ogc:Within>
                    <ogc:PropertyName>myns:track</ogc:PropertyName>
                    <gml:Envelope srsName="...">
                        <gml:lowerCorner>50 40</gml:lowerCorner>
                        <gml:upperCorner>100 60</gml:upperCorner>
                    </gml:Envelope>
                </ogc:Within>
          </ogc:Filter>
    </Query>
        </GetFeature>
    
    
    def tearDown(self):
        ''' '''





if __name__ == '__main__':
    unittest.main()
