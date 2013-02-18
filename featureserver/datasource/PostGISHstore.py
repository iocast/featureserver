
import re
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

    def get_predicate(self, constraint):
        if constraint.operator.lower() in self.query_actions:
            if constraint.operator.lower() == 'like':
                return self.find_hstore_attribute(constraint.attribute) + " " + self.query_actions[constraint.operator.lower()] + " '%" + constraint.value + "%'"
            
            elif constraint.operator.lower() == 'bbox':
                return self.query_actions['bbox'].format(**{'geometry':self.geom_col, 'bbox':constraint.value, 'srs':self.srid, 'srs_out':self.srid_out})
            
            return self.find_hstore_attribute(constraint.attribute) + " " + self.query_actions[constraint.operator.lower()] + " '" + constraint.value + "'"
        raise PredicateNotFoundException(**{'locator':self.__class__.__name__, 'predicate':constraint.operator})

    def find_hstore_attribute(self, attribute):
        for value in self.attribute_cols.split(","):
            if re.search(r'"'+attribute+'"$', value):
                return value[:value.find(' as "')]

        for value in self.additional_cols.split(","):
            if re.search(r'"'+attribute+'"$', value):
                return value[:value.find(' as "')]
        
        return attribute

