'''
Created on Oct 22, 2012
    
@author: michel
'''

from FeatureServer.DataSource import DataSource
from vectorformats.Feature import Feature
from vectorformats.Formats import WKT

from pyspatialite import dbapi2 as db

import datetime


class SpatialLite (DataSource):

    def __init__(self, name, file, fid = "fid", geometry = "geometry", order = "", srid = 4326, srid_out = 4326, writable = True, attribute_cols = "*", **kwargs):
        DataSource.__init__(self, name, **kwargs)
        self.file           = file
        self.table          = kwargs["layer"]
        self.fid_col        = fid
        self.geom_col       = geometry
        self.srid           = srid
        self.srid_out       = srid_out
        self.writable       = writable
        self.attribute_cols = attribute_cols
        self.order          = order

    def begin(self):
        self._connection = db.connect(self.file)

    def commit(self):
        if self.writable:
            self._connection.commit()
        self._connection.close()

    def rollback(self):
        if self.writable:
            self._connection.rollback()
        self._connection.close()

    
    def insert(self, action, response=None):
        ''' '''

    def update(self, action, response=None):
        ''' '''

    def delete(self, action, response=None):
        ''' '''

    def select(self, action, response=None):
        cursor = self._connection.cursor()
        
        if action.id is not None:
            sql = "SELECT AsText(Transform(%s, %d)) as fs_text_geom, " % (self.geom_col, int(self.srid_out))

            if hasattr(self, 'version'):
                sql += "%s as version, " % self.version
            if hasattr(self, 'ele'):
                sql += "%s as ele, " % self.ele
            
            sql += "\"%s\", %s" % (self.fid_col, self.attribute_cols)

            if hasattr(self, "additional_cols"):
                cols = self.additional_cols.split(';')
                additional_col = ",".join(cols)
                sql += ", %s" % additional_col
                
            sql += " FROM \"%s\" WHERE %s = :%s" % (self.table, self.fid_col, self.fid_col)

            cursor.execute(str(sql), {self.fid_col: str(action.id)})
            
            result = [cursor.fetchone()]
            
        else:
            filters = []
            attrs = []
            if action.attributes:
                match = Feature(props = action.attributes)
                filters = self.feature_predicates(match)
                for key, value in action.attributes.items():
                    if isinstance(value, dict):
                        attrs[key] = value['value']
                    else:
                        attrs[key] = value
            if action.bbox:
                filters.append( "%s && Transform(SetSRID('BOX3D(%f %f,%f %f)'::box3d, %s), %s) AND intersects(%s, Transform(SetSRID('BOX3D(%f %f,%f %f)'::box3d, %s), %s))" % ((self.geom_col,) + tuple(action.bbox) + (self.srid_out,) + (self.srid,) + (self.geom_col,) + (tuple(action.bbox) + (self.srid_out,) + (self.srid,))))
            sql = "SELECT AsText(Transform(%s, %d)) as fs_text_geom, " % (self.geom_col, int(self.srid_out))
            if hasattr(self, 'ele'):
                sql += "%s as ele, " % self.ele
            if hasattr(self, 'version'):
                sql += "%s as version, " % self.version
            sql += "\"%s\", %s" % (self.fid_col, self.attribute_cols)
            
            if hasattr(self, "additional_cols"):
                cols = self.additional_cols.split(';')
                additional_col = ",".join(cols)
                sql += ", %s" % additional_col
            
            sql += " FROM \"%s\"" % (self.table)
            
            if filters:
                sql += " WHERE " + " AND ".join(filters)
            if action.wfsrequest:
                if filters:
                    sql += " AND "
                else:
                    sql += " WHERE "
                
                sql += action.wfsrequest.render(self)
            
            
            if self.order:
                sql += " ORDER BY " + self.order
            if action.maxfeatures:
                sql += " LIMIT %d" % action.maxfeatures
            #else:
            #    sql += " LIMIT 1000"
            if action.startfeature:
                sql += " OFFSET %d" % action.startfeature
            
            cursor.execute(str(sql), attrs)

            result = cursor.fetchall()
                
        columns = [desc[0] for desc in cursor.description]
        features = []
        for row in result:
            props = dict(zip(columns, row))
            if not props['fs_text_geom']: continue
            geom  = WKT.from_wkt(props['fs_text_geom'])
            id = props[self.fid_col]
            del props[self.fid_col]
            if self.attribute_cols == '*':
                del props[self.geom_col]
            del props['fs_text_geom']
            for key, value in props.items():
                if isinstance(value, str):
                    props[key] = unicode(value, self.encoding)
                elif isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
                    # stringify datetimes
                    props[key] = str(value)

                try:
                    if isinstance(value, decimal.Decimal):
                        props[key] = unicode(str(value), self.encoding)
                except:
                    pass

            if (geom):
                features.append( Feature( id, geom, self.geom_col, self.srid_out, props ) )
        return features

    

    def getAttributeDescription(self, attribute):
        ''' '''

