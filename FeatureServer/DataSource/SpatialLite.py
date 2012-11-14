'''
Created on Oct 22, 2012
    
@author: michel
'''

import os

from DataSource import DataSource
from VectorFormats.Feature import Feature
from VectorFormats.Formats import WKT

from FeatureServer.Parsers.WebFeatureService.Response.InsertResult import InsertResult
from FeatureServer.Parsers.WebFeatureService.Response.UpdateResult import UpdateResult
from FeatureServer.Parsers.WebFeatureService.Response.DeleteResult import DeleteResult
from FeatureServer.Parsers.WebFeatureService.Response.ReplaceResult import ReplaceResult


from pyspatialite import dbapi2 as db

import datetime

from FeatureServer.Exceptions.ConnectionException import ConnectionException


class SpatialLite (DataSource):
    
    query_action_types = ['lt', 'gt', 'ilike', 'like', 'gte', 'lte']
    
    query_action_sql = {'lt': '<', 'gt': '>',
        'ilike': 'ilike', 'like':'like',
        'gte': '>=', 'lte': '<='}

    def __init__(self, name, file, fid = "gid", geometry = "geometry", fe_attributes = 'true', order = "", srid = 4326, srid_out = 4326, encoding = "utf-8", writable = True, attribute_cols = "*", **kwargs):
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
        self.encoding       = encoding

        self.fe_attributes = True
        if fe_attributes.lower() == 'false':
            self.fe_attributes  = False
    

    def column_names (self, feature):
        return feature.properties.keys()
    
    def value_formats (self, feature):
        values = ["%%(%s)s" % self.getGeometry()]
        values = []
        for key, val in feature.properties.items():
            valtype = type(val).__name__
            if valtype == "dict":
                val['pred'] = "%%(%s)s" % (key,)
                values.append(val)
            else:
                fmt     = "%%(%s)s" % (key, )
                values.append(fmt)
        return values
    
    
    def feature_predicates (self, feature):
        columns = self.column_names(feature)
        values  = self.value_formats(feature)
        predicates = []
        for pair in zip(columns, values):
            if pair[0] != self.getGeometry():
                if isinstance(pair[1], dict):
                    # Special Query: pair[0] is 'a', pair[1] is {'type', 'pred', 'value'}
                    # We build a Predicate here, then we replace pair[1] with pair[1] value below
                    if pair[1].has_key('value'):
                        predicates.append("%s %s %s" % (pair[1]['column'],
                                                        self.query_action_sql[pair[1]['type']],
                                                        pair[1]['pred']))
                
                else:
                    predicates.append("%s = %s" % pair)
        if feature.geometry and feature.geometry.has_key("coordinates"):
            predicates.append(" %s = SetSRID('%s'::geometry, %s) " % (self.getGeometry(), WKT.to_wkt(feature.geometry), self.srid))
        return predicates
    
    def feature_values (self, feature):
        props = copy.deepcopy(feature.properties)
        for key, val in props.iteritems():
            if type(val) is unicode:
                props[key] = val.encode(self.encoding)
            if type(val)  is dict:
                props[key] = val['value']
        return props

    
    def begin(self):
        if not os.path.exists(self.file):
            raise ConnectionException(**{'layer':self.name,'locator':'SpatialLite'})
        self._connection = db.connect(self.file, check_same_thread = False)
    
    def close(self):
        self._connection.close()

    def commit(self):
        if self.writable:
            self._connection.commit()
        self.close()

    def rollback(self):
        if self.writable:
            self._connection.rollback()
        self.close()

    def insert(self, action):
        self.begin()
        
        sql = action.get_statement()
        print sql
        return
            
        cursor = self._connection.cursor()
        cursor.execute(str(sql))
            
        cursor.execute("SELECT last_insert_rowid()")
        action.id =  cursor.fetchone()[0]
            
        return InsertResult(action.id, "")
            

    def update(self, action):
        self.begin()

        sql = action.get_statement()
        print sql
        return
        cursor = self._connection.cursor()
        cursor.execute(str(sql))
            
        return UpdateResult(action.id, "")


    def delete(self, action):
        self.begin()

        sql = action.get_statement()
        print sql
        return
        cursor = self._connection.cursor()
        cursor.execute(str(sql))
        
        return DeleteResult(action.id, "")
        

    def select(self, action):
        self.begin()
        cursor = self._connection.cursor()
        
        sql = "SELECT AsText(Transform(%s, %d)) as fs_text_geom, " % (self.getGeometry(), int(self.srid_out))
        
        
        # add attributes from config file
        if hasattr(self, 'version'):
            sql += "%s as version, " % self.version
        if hasattr(self, 'ele'):
            sql += "%s as ele, " % self.ele
            
        sql += "\"%s\"" % self.fid_col
            
        if len(self.attribute_cols) > 0:
            sql += ", %s" % self.attribute_cols
            
        if hasattr(self, "additional_cols"):
            cols = self.additional_cols.split(';')
            additional_col = ",".join(cols)
            sql += ", %s" % additional_col
                
                
        # add attributes from parser
        if action.get_attributes() is not None and len(action.get_attributes()) > 0:
            fe_cols = action.get_attributes()
            ad_cols = self.getColumns()
            # removes attributes that already are defined in the configuration file
            fe_cols = filter(lambda x: x not in ad_cols, fe_cols)
            
            if len(fe_cols) > 0:
                sql += ", %s" % ",".join(fe_cols)

        sql += " FROM \"%s\"" % (self.table)
        
        
        if action.get_statement() is not None:
            sql += " WHERE " + action.get_statement()
    
        print sql
        return []
        
        cursor.execute(str(sql))
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
                del props[self.getGeometry()]
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
                features.append( Feature( action.layer, id, geom, self.getGeometry(), self.srid_out, props ) )
        
        return features
    
    
    def getColumns(self):
        cols = []

        if hasattr(self, 'attribute_cols'):
            cols = self.attribute_cols.split(",")
        
        cols.append(self.getGeometry())
        cols.append(self.fid_col)
        
        if hasattr(self, 'version'):
            cols.append(self.version)
        if hasattr(self, 'ele'):
            cols.append(self.ele)
        
        return cols
    
    def getGeometry(self):
        return self.geom_col
    def getAttributes(self):
        return self.attribute_cols
        
    
    def getAttributeDescription(self, attribute):
        self.begin()
        cursor = self._connection.cursor()
        result = []
        
        sql = "PRAGMA table_info(%s)"
        
        try:
            cursor.execute(sql % self.table)
            result = cursor.fetchall()
            self.commit()
        except:
            pass
        
    
        type = 'string'
        length = ''
        
        if len(result) > 0:
            for col in result:
                if col[1] == attribute:
                    if str(col[2]).lower().startswith('int'):
                        type = 'integer'
                        length = ''
                        break
    
        return (type, length)
