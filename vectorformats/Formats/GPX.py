'''
Created on Jul 30, 2011

@author: michel
'''

from vectorformats.Formats.Format import Format
from xml.sax.saxutils import escape
import types

class GPX(Format):
    
    def encode(self, features, **kwargs):
        results = ["""<?xml version="1.0" encoding="UTF-8"?>
        <gpx version="1.0">"""]
        results.append("<name>%s</name>" % self.layername) 
        
        for feature in features:
            results.append(self.encode_feature(feature))
        
        results.append("</gpx>")
        return "\n".join(results)
        
    def encode_feature(self, feature):
        xml = []
        
        if feature.geometry['type'] == 'Point':
            xml.append("""<wpt lon="%s" lat="%s">""" % (str(feature.geometry["coordinates"][0]), str(feature.geometry["coordinates"][1])))
            if feature.properties.has_key('name'):
                if isinstance(feature.properties["name"], types.NoneType):
                    xml.append("""<name>%s</name>""" % str(feature.id))
                else:
                    xml.append("""<name>%s</name>""" % escape(feature.properties["name"]))
            else:
                xml.append("""<name>%s</name>""" % str(feature.id))
            if feature.properties.has_key('ele'):
                xml.append("""<ele>%s</ele>""" % feature.properties["ele"])
            xml.append("""</wpt>""")
            
        return "\n".join(xml)
        