__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: PostGIS.py 615 2009-09-23 00:47:48Z jlivni $"

from psycopg2 import errorcodes

from DataSource import DataSource
from vectorformats.feature import Feature
from vectorformats.formats import wkt

from ..parsers.WebFeatureService.Response.InsertResult import InsertResult
from ..parsers.WebFeatureService.Response.UpdateResult import UpdateResult
from ..parsers.WebFeatureService.Response.DeleteResult import DeleteResult
from ..parsers.WebFeatureService.Response.ReplaceResult import ReplaceResult

from ..exceptions.wfs import InvalidValueException
from ..exceptions.datasource import ConnectionException

try:
    import psycopg2 as psycopg
    
except:
    import psycopg

import copy
import re
import datetime

try:
    import decimal
except:
    pass
    
class PostGIS (DataSource):
    """PostGIS datasource. Setting up the table is beyond the scope of
       FeatureServer."""
    
    query_action_types = ['lt', 'gt', 'ilike', 'like', 'gte', 'lte']

    query_action_sql = {'lt': '<', 'gt': '>', 
                        'ilike': 'ilike', 'like':'like',
                        'gte': '>=', 'lte': '<='}
     
    def __init__(self, name, srid = 4326, srid_out = 4326, fid = "gid", geometry = "the_geom", fe_attributes = 'true', order = "", attribute_cols = '*', writable = True, encoding = "utf-8", **kwargs):
        super(PostGIS, self).__init__(name, **kwargs)
        self.table          = kwargs["layer"]
        self.fid_col        = fid
        self.encoding       = encoding
        self.geom_col       = geometry
        self.order          = order
        self.srid           = srid
        self.srid_out       = srid_out
        self.db             = None
        self.dsn            = kwargs["dsn"]
        self.writable       = writable
        self.attribute_cols = attribute_cols
        
        self.fe_attributes = True
        if fe_attributes.lower() == 'false':
            self.fe_attributes  = False

    def begin (self):
        try:
            self.db = psycopg.connect(self.dsn)
        except Exception as e:
            raise ConnectionException(**{'dump':str(e),'layer':self.name,'locator':'PostGIS','code':e.pgcode})
    
    def commit (self):
        if self.db:
            if self.writable:
                self.db.commit()
            self.db.close()

    def rollback (self):
        if self.db:
            if self.writable and self.db:
                self.db.rollback()
            self.db.close()

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
            predicates.append(" %s = SetSRID('%s'::geometry, %s) " % (self.getGeometry(), wkt.to_wkt(feature.geometry), self.srid))
        return predicates

    def feature_values (self, feature):
        props = copy.deepcopy(feature.properties)
        for key, val in props.iteritems():
            if type(val) is unicode: ### b/c psycopg1 doesn't quote unicode
                props[key] = val.encode(self.encoding)
            if type(val)  is dict:
                props[key] = val['value']
        return props


    def id_sequence (self):
        return self.table + "_" + self.fid_col + "_seq"
    
    def insert (self, action):
        sql = action.statement
        
        cursor = self.db.cursor()
        try:
            cursor.execute(str(sql))
        except Exception as e:
            raise SyntaxException(locator = self.__class__.__name__, dump = str(e))
        
        cursor.execute("SELECT currval('%s');" % self.id_sequence())
        id = cursor.fetchone()[0]
        
        result = InsertResult("")
        result.add(id)
        
        return result
    
    
    def update (self, action):
        sql = action.statement
        
        cursor = self.db.cursor()
        try:
            cursor.execute(str(sql))
        except Exception as e:
            raise SyntaxException(locator = self.__class__.__name__, dump = str(e))
        
        result = UpdateResult("")
        result.extend(action.ids)
        
        return result

        
    def delete (self, action):
        sql = action.statement
        
        cursor = self.db.cursor()
        try:
            cursor.execute(str(sql))
        except Exception as e:
            raise SyntaxException(locator = self.__class__.__name__, dump = str(e))
        
        result = DeleteResult("")
        result.extend(action.ids)
        
        return result
    
        
    def select (self, action):
        cursor = self.db.cursor()
        
        sql = "SELECT ST_AsText(ST_Transform(%s, %d)) as fs_text_geom, " % (self.getGeometry(), int(self.srid_out))
        
        # add attributes from config file
        if hasattr(self, 'version'):
            sql += "%s as version, " % self.version
        if hasattr(self, 'ele'):
            sql += "%s as ele, " % self.ele

        sql += "\"%s\"" % self.fid_col

        if len(self.attribute_cols) > 0:
            sql += ", %s" % self.attribute_cols

        if hasattr(self, "additional_cols") and len(self.additional_cols) > 0:
            cols = self.additional_cols.split(';')
            additional_col = ",".join(cols)
            sql += ", %s" % additional_col


        # add attributes from parser
        if self.fe_attributes:
            if action.attributes is not None and len(action.attributes) > 0:
                ad_cols = self.getColumns()
                # removes attributes that already are defined in the configuration file
                fe_cols = filter(lambda x: x not in ad_cols, action.attributes)
    
                if len(fe_cols) > 0:
                    sql += ", %s" % ",".join(fe_cols)

        sql += " FROM \"%s\"" % (self.table)
        
        
        if action.statement is not None:
            sql += " WHERE " + action.statement
                    
        if self.order:
            sql += " ORDER BY " + self.order
            
        try:
            cursor.execute(str(sql))
        except Exception as e:
            if e.pgcode[:2] == errorcodes.CLASS_SYNTAX_ERROR_OR_ACCESS_RULE_VIOLATION:
                raise InvalidValueException(**{'dump':e.pgerror,'layer':self.name,'locator':'PostGIS'})
            
        result = cursor.fetchall()
        

        columns = [desc[0] for desc in cursor.description]
        features = []
        for row in result:
            props = dict(zip(columns, row))
            if not props['fs_text_geom']: continue
            geom  = wkt.from_wkt(props['fs_text_geom'])
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
                features.append( Feature( layer=action.layer, id=id, geometry=geom, geometry_attr=self.getGeometry(), srs=self.srid_out, props=props ) )

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
        cursor = self.db.cursor()
        result = []

        sql = "SELECT t.typname AS type, a.attlen AS length FROM pg_class c, pg_attribute a, pg_type t "
        sql += "WHERE c.relname = '%s' and a.attname = '%s' and a.attnum > 0 and a.attrelid = c.oid and a.atttypid = t.oid ORDER BY a.attnum"
        
        try:
            cursor.execute(str(sql)% (self.table, attribute))
            result = [cursor.fetchone()]
            self.db.commit()
        except:
            pass 
        
        type = 'string'
        length = ''
        
        if len(result) > 0:
            if result[0]:
                if str((result[0])[0]).lower().startswith('int'):
                    type = 'integer'
                    if int((result[0])[1]) == 4:
                        length = ''
        
        return (type, length)
