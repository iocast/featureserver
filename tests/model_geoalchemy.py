from sqlalchemy import create_engine, MetaData, Column, Integer, String, Numeric, DateTime, Unicode
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from geoalchemy import GeometryColumn, LineString, Polygon, Point, GeometryCollection, GeometryDDL, WKTSpatialElement
from geoalchemy.functions import functions
from geoalchemy.postgis import pg_functions

from datetime import datetime

engine = create_engine('sqlite:///:memory:', echo=False)
session = sessionmaker(bind=engine)()
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

class FSPoint(Base):
    __tablename__ = 'fs_point'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    salary = Column(Integer)
    geom = GeometryColumn(Point(2))

GeometryDDL(FSPoint.__table__)
