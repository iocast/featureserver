import re
from lxml import etree

from vectorformats.formats.wfs import WFS as WFSVectorFormat

class WFS (WFSVectorFormat):

    def get_capabilities(self):
        tree = etree.parse("featureserver/assets/transformation/wfs-capabilities.xml")
        root = tree.getroot()
        elements = root.xpath("wfs:Capability/wfs:Request/wfs:GetCapabilities/wfs:DCPType/wfs:HTTP", namespaces = self.namespaces)
        if len(elements) > 0:
            for element in elements:
                for http in element:
                    http.set('onlineResource', self.service.request.host + '?')
        
        elements = root.xpath("wfs:Capability/wfs:Request/wfs:DescribeFeatureType/wfs:DCPType/wfs:HTTP", namespaces = self.namespaces)
        if len(elements) > 0:
            for element in elements:
                for http in element:
                    http.set('onlineResource', self.service.request.host + '?')
        
        elements = root.xpath("wfs:Capability/wfs:Request/wfs:GetFeature/wfs:DCPType/wfs:HTTP", namespaces = self.namespaces)
        if len(elements) > 0:
            for element in elements:
                for http in element:
                    http.set('onlineResource', self.service.request.host + '?')
        
        elements = root.xpath("wfs:Capability/wfs:Request/wfs:Transaction/wfs:DCPType/wfs:HTTP", namespaces = self.namespaces)
        if len(elements) > 0:
            for element in elements:
                for http in element:
                    http.set('onlineResource', self.service.request.host + '?')
        
        
        layers = self.getlayers()
        featureList = root.xpath("wfs:FeatureTypeList", namespaces = self.namespaces)
        if len(featureList) > 0 and len(layers) > 0:
            for layer in layers:
                featureList[0].append(layer)
        
        return etree.tostring(tree, pretty_print=True)
    
    def getlayers(self):
        ''' '''
        featureList = etree.Element('FeatureTypeList')
        operations = etree.Element('Operations')
        operations.append(etree.Element('Query'))
        featureList.append(operations)
        
        for layer in self.service.datasources:
            type = etree.Element('FeatureType')
            name = etree.Element('Name')
            name.text = layer
            type.append(name)
            
            title = etree.Element('Title')
            if hasattr(self.datasources[layer], 'title'):
                title.text = self.datasources[layer].title
            type.append(title)
            
            abstract = etree.Element('Abstract')
            if hasattr(self.datasources[layer], 'abstract'):
                abstract.text = self.datasources[layer].abstract
            type.append(abstract)
            
            
            srs = etree.Element('SRS')
            if hasattr(self.datasources[layer], 'srid_out') and self.datasources[layer].srid_out is not None:
                srs.text = 'EPSG:' + str(self.datasources[layer].srid_out)
            else:
                srs.text = 'EPSG:4326'
            type.append(srs)
            
            featureOperations = etree.Element('Operations')
            featureOperations.append(etree.Element('Insert'))
            featureOperations.append(etree.Element('Update'))
            featureOperations.append(etree.Element('Delete'))
            type.append(featureOperations)
            
            latlong = self.getBBOX(self.datasources[layer])
            type.append(latlong)
            
            featureList.append(type)
        
        return featureList
    
    def describe_feature_type(self):
        tree = etree.parse("resources/wfs-featuretype.xsd")
        root = tree.getroot()
        
        if len(self.layers) == 1:
            ''' special case when only one datasource is requested --> other xml schema '''
            root = self.addDataSourceFeatureType(root, self.datasources[self.layers[0]])
        else:
            ''' loop over all requested datasources '''
            for layer in self.layers:
                root = self.addDataSourceImport(root, self.datasources[layer])
        #root = self.addDataSourceFeatureType(root, self.datasources[layer])
        
        return etree.tostring(tree, pretty_print=True)
    
    def addDataSourceImport(self, root, datasource):
        root.append(
                    etree.Element('import', attrib={'namespace':self.namespaces['fs'],
                                  'schemaLocation':self.host+'?request=DescribeFeatureType&typeName='+datasource.name})
                    )
        return root
    
    def addDataSourceFeatureType(self, root, datasource):
        
        root.append(etree.Element('element', attrib={'name':datasource.name,
                                  'type':'fs:'+datasource.name+'_Type',
                                  'substitutionGroup':'gml:_Feature'}))
        
        complexType = etree.Element('complexType', attrib={'name':datasource.name+'_Type'})
        complexContent = etree.Element('complexContent')
        extension = etree.Element('extension', attrib={'base':'gml:AbstractFeatureType'})
        sequence = etree.Element('sequence')
        
        for attribut_col in datasource.attribute_cols.split(','):
            type, length = datasource.getAttributeDescription(attribut_col)
            
            maxLength = etree.Element('maxLength', attrib={'value':str(length)})
            restriction = etree.Element('restriction', attrib={'base' : type})
            restriction.append(maxLength)
            simpleType = etree.Element('simpleType')
            simpleType.append(restriction)
            
            attrib_name = attribut_col
            if hasattr(datasource, "hstore"):
                if datasource.hstore:
                    attrib_name = self.getFormatedAttributName(attrib_name)
            
            element = etree.Element('element', attrib={'name' : str(attrib_name),
                                    'minOccurs' : '0'})
            element.append(simpleType)
            
            sequence.append(element)
        
        if hasattr(datasource, "additional_cols"):
            for additional_col in datasource.additional_cols.split(';'):
                name = additional_col
                matches = re.search('(?<=[ ]as[ ])\s*\w+', str(additional_col))
                if matches:
                    name = matches.group(0)
                
                type, length = datasource.getAttributeDescription(name)
                
                maxLength = etree.Element('maxLength', attrib={'value':'0'})
                restriction = etree.Element('restriction', attrib={'base' : type})
                restriction.append(maxLength)
                simpleType = etree.Element('simpleType')
                simpleType.append(restriction)
                element = etree.Element('element', attrib={'name' : name,
                                        'minOccurs' : '0',
                                        'maxOccurs' : '0'})
                element.append(simpleType)
                
                sequence.append(element)


        if hasattr(datasource, 'geometry_type'):
            properties = datasource.geometry_type.split(',')
        else:
            properties = ['Point', 'Line', 'Polygon']
        for property in properties:
            if property == 'Point':
                element = etree.Element('element', attrib={'name' : datasource.geom_col,
                                        'type' : 'gml:PointPropertyType',
                                        'minOccurs' : '0'})
                sequence.append(element)
            elif property == 'Line':
                element = etree.Element('element', attrib={'name' : datasource.geom_col,
                                        'type' : 'gml:LineStringPropertyType',
                                        #'ref' : 'gml:curveProperty',
                                        'minOccurs' : '0'})
                sequence.append(element)
            elif property == 'Polygon':
                element = etree.Element('element', attrib={'name' : datasource.geom_col,
                                        'type' : 'gml:PolygonPropertyType',
                                        #'substitutionGroup' : 'gml:_Surface',
                                        'minOccurs' : '0'})
                sequence.append(element)


        extension.append(sequence)
        complexContent.append(extension)
        complexType.append(complexContent)
        root.append(complexType)

        return root
    
    def getBBOX(self, datasource):
        if hasattr(datasource, 'bbox'):
            latlong = datasource.bbox
        else:
            latlong = datasource.getBBOX()
        latlongArray = latlong.split(' ')
        
        return etree.Element('bbox',
                             attrib={'minx':latlongArray[0],
                             'miny':latlongArray[1],
                             'maxx':latlongArray[2],
                             'maxy':latlongArray[3]})


