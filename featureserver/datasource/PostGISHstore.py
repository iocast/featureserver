
from PostGIS import PostGIS

class PostGISHstore (PostGIS):
    
    @property
    def hstore_attribute(self):
        return self.hstore_attr

    def __init__(self, name, hstore, **kwargs):
        super(PostGISHstore, self).__init__(name, **kwargs)
        self.hstore_attr    = hstore

    def getFormatedAttributName(self, name):
        attrib_name = name
        
        attrib_pos = name.find(' as "')
        if attrib_pos >= 0:
            attrib_name = name[attrib_pos+5:-1]
        
        return attrib_name
    