import unittest

from featureserver.server import Server
from featureserver.web_request.response import Response
from featureserver.web_request.request import Request

from featureserver.datasource.GeoAlchemy import GeoAlchemy


class WFSTestCase(unittest.TestCase):
    
    @property
    def fs(self):
        return self._fs
    
    @classmethod
    def setUpClass(cls):
        params = {
            'model': 'tests.model_geoalchemy',
            'dburi': 'postgres://michel@localhost/featureserver',
            'cls': 'Road',
            'fid': 'id',
            'geometry': 'geom'
        }
        
        ds = GeoAlchemy('roads', **params)
        cls._fs = Server({'roads': ds})
    
    @classmethod
    def tearDownClass(cls):
        ''' '''
    
    def test_keyword_capabilities(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/capabilities.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(response.data.replace("\n", "").replace("\t", ""), self.data_capability)
    
    def test_keyword_describe_feature_type(self):
        response = self.fs.dispatchRequest(Request(base_path = "", path_info = "/wfs/roads/describe.wfs", params = {'version':'1.1.0'}))
        self.assertEqual(response.data.replace("\n", "").replace("\t", ""), self.data_describe_feature_type)

    
    
    @property
    def data_capability(self):
        return '<WFS_Capabilities xmlns="http://www.opengis.net/wfs" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0"><Service><Name>WFS Server</Name><Title>Web Feature Service Server</Title><Abstract>Supports&#160;WFS, GML, KML, etc.</Abstract><OnlineResource/></Service><Capability><Request><GetCapabilities><DCPType><HTTP><Get onlineResource="?"/></HTTP></DCPType></GetCapabilities><DescribeFeatureType><SchemaDescriptionLanguage><XMLSCHEMA/></SchemaDescriptionLanguage><DCPType><HTTP><Get onlineResource="?"/></HTTP></DCPType></DescribeFeatureType><GetFeature><ResultFormat><GML2/></ResultFormat><DCPType><HTTP><Get onlineResource="?"/></HTTP></DCPType></GetFeature><Transaction><ResultFormat><GML2/></ResultFormat><DCPType><HTTP><Post onlineResource="?"/></HTTP></DCPType></Transaction></Request></Capability><FeatureTypeList><Operations><Query/></Operations></FeatureTypeList><SupportsGMLObjectTypeList><GMLObjectType><Name>gml:AbstractGMLFeatureType</Name><OutputFormats><Format>text/xml; subtype=gml/2.1.2</Format><Format>text/xml; subtype=gml/3.1.1</Format></OutputFormats></GMLObjectType><GMLObjectType><Name>gml:PointType</Name><OutputFormats><Format>text/xml; subtype=gml/2.1.2</Format><Format>text/xml; subtype=gml/3.1.1</Format></OutputFormats></GMLObjectType><GMLObjectType><Name>gml:LineStringType</Name><OutputFormats><Format>text/xml; subtype=gml/2.1.2</Format><Format>text/xml; subtype=gml/3.1.1</Format></OutputFormats></GMLObjectType><GMLObjectType><Name>gml:PolygonType</Name><OutputFormats><Format>text/xml; subtype=gml/2.1.2</Format><Format>text/xml; subtype=gml/3.1.1</Format></OutputFormats></GMLObjectType><GMLObjectType><Name>gml:MultiPointType</Name><OutputFormats><Format>text/xml; subtype=gml/2.1.2</Format><Format>text/xml; subtype=gml/3.1.1</Format></OutputFormats></GMLObjectType><GMLObjectType><Name>gml:MultiLineStringType</Name><OutputFormats><Format>text/xml; subtype=gml/2.1.2</Format><Format>text/xml; subtype=gml/3.1.1</Format></OutputFormats></GMLObjectType><GMLObjectType><Name>gml:MultiPolygonType</Name><OutputFormats><Format>text/xml; subtype=gml/2.1.2</Format><Format>text/xml; subtype=gml/3.1.1</Format></OutputFormats></GMLObjectType></SupportsGMLObjectTypeList><ogc:Filter_Capabilities><ogc:Spatial_Capabilities><ogc:GeometryOperands><ogc:GeometryOperand>gml:Envelope</ogc:GeometryOperand><ogc:GeometryOperand>gml:Point</ogc:GeometryOperand><ogc:GeometryOperand>gml:LineString</ogc:GeometryOperand><ogc:GeometryOperand>gml:Polygon</ogc:GeometryOperand></ogc:GeometryOperands><ogc:SpatialOperators><ogc:SpatialOperator name="Disjoint"/><ogc:SpatialOperator name="Equals"/><ogc:SpatialOperator name="DWithin"/><ogc:SpatialOperator name="Beyond"/><ogc:SpatialOperator name="Intersects"/><ogc:SpatialOperator name="Touches"/><ogc:SpatialOperator name="Crosses"/><ogc:SpatialOperator name="Within"/><ogc:SpatialOperator name="Contains"/><ogc:SpatialOperator name="Overlaps"/><ogc:SpatialOperator name="BBOX"/></ogc:SpatialOperators></ogc:Spatial_Capabilities><ogc:Scalar_Capabilities><ogc:Logical_Operators/><ogc:Comparison_Operators><ogc:ComparisonOperator>EqualTo</ogc:ComparisonOperator><ogc:ComparisonOperator>NotEqualTo</ogc:ComparisonOperator><ogc:ComparisonOperator>LessThan</ogc:ComparisonOperator><ogc:ComparisonOperator>GreaterThan</ogc:ComparisonOperator><ogc:ComparisonOperator>LessThanEqualTo</ogc:ComparisonOperator><ogc:ComparisonOperator>GreaterThanEqualTo</ogc:ComparisonOperator><ogc:ComparisonOperator>Between</ogc:ComparisonOperator><ogc:ComparisonOperator>Like</ogc:ComparisonOperator><ogc:ComparisonOperator>NullCheck</ogc:ComparisonOperator></ogc:Comparison_Operators><ogc:Arithmetic_Operators><ogc:Simple_Arithmetic/><ogc:Functions></ogc:Functions></ogc:Arithmetic_Operators></ogc:Scalar_Capabilities></ogc:Filter_Capabilities></WFS_Capabilities>'

    @property
    def data_describe_feature_type(self):
        return '<schema xmlns:fs="http://featureserver.org/fs" xmlns="http://www.w3.org/2001/XMLSchema" xmlns:gml="http://www.opengis.net/gml" targetNamespace="http://featureserver.org/fs" elementFormDefault="qualified" attributeFormDefault="unqualified" version="0.1"><import namespace="http://www.opengis.net/gml" schemaLocation="http://schemas.opengis.net/gml/2.0.0/feature.xsd"/><element substitutionGroup="gml:_Feature" type="fs:roads_Type" name="roads"/><complexType name="roads_Type"><complexContent><extension base="gml:AbstractFeatureType"><sequence><element name="*" minOccurs="0"><simpleType><restriction base="string"><maxLength value=""/></restriction></simpleType></element><element type="gml:PointPropertyType" name="geom" minOccurs="0"/><element type="gml:LineStringPropertyType" name="geom" minOccurs="0"/><element type="gml:PolygonPropertyType" name="geom" minOccurs="0"/></sequence></extension></complexContent></complexType></schema>'

def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(WFSTestCase)