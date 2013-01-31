__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: PostGIS.py 615 2009-09-23 00:47:48Z jlivni $"

from psycopg2 import errorcodes

from DataSource import DataSource
from vectorformats.feature import Feature
from vectorformats.formats import wkt

from ..parsers.web_feature_service.response.action_result import InsertResult, UpdateResult, DeleteResult, ReplaceResult

from ..exceptions.wfs import InvalidValueException
from ..exceptions.syntax import SyntaxException
from ..exceptions.datasource import ConnectionException, PredicateNotFoundException

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
    
    _query_actions  = { 'eq' : '=', 'neq' : '!=',
                        'lt' : '<', 'gt' : '>',
                        'gte': '>=', 'lte': '<=',
                        'like' : 'LIKE',
                        'bbox' : 'ST_Intersects("{geometry!s}", ST_Transform(ST_MakeEnvelope({bbox[0]:f}, {bbox[1]:f}, {bbox[2]:f}, {bbox[3]:f}, {srs_out:d}), {srs:d}))'
                        }
    
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
    
    def commit (self, close=True):
        if self.db:
            if self.writable:
                self.db.commit()
            if close:
                self.close()

    def rollback (self, close=True):
        if self.db:
            if self.writable and self.db:
                self.db.rollback()
            if close:
                self.close()

    def close (self):
        if self.db:
            self.db.close()
    

    def get_predicate(self, constraint):
        if constraint.operator.lower() in self.query_actions:
            if constraint.operator.lower() == 'like':
                return "\"" + constraint.attribute + "\" " + self.query_actions[constraint.operator.lower()] + " '%" + constraint.value + "%'"
            
            elif constraint.operator.lower() == 'bbox':
                return self.query_actions['bbox'].format(**{'geometry':self.geom_col, 'bbox':constraint.value, 'srs':self.srid, 'srs_out':self.srid_out})
        
            return "\"" + constraint.attribute + "\" " + self.query_actions[constraint.operator.lower()] + " '" + constraint.value + "'"
        raise PredicateNotFoundException(**{'locator':self.__class__.__name__, 'predicate':constraint.operator})
    

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

        print sql

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
        
        where = []
        if action.statement is not None:
            where.append(action.statement)
        
        for constraint in action.constraints:
            where.append(self.get_predicate(constraint))
                
        for id in action.ids:
            where.append("\"%s\" = '%s'" % (self.fid_col, str(id)))
        
        if len(where) > 0:
            sql += " WHERE "
            sql += " AND ".join(where)

        if len(action.sort) > 0:
            sql += " ORDER BY "
            for sort in action.sort:
                sql += "%s %s, " % (sort.attribute, sort.operator)
            sql = sql[:-2]

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
