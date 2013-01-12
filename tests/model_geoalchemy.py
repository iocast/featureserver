from sqlalchemy import create_engine, MetaData, Column, Integer, String, Numeric, DateTime, Unicode
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from geoalchemy import GeometryColumn, LineString, Polygon, Point, GeometryCollection, GeometryDDL, WKTSpatialElement
from geoalchemy.functions import functions
from geoalchemy.postgis import pg_functions

from datetime import datetime

engine = create_engine('postgres://michel@localhost/featureserver', echo=False)
session = sessionmaker(bind=engine)()
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

class Road(Base):
    __tablename__ = 'roads'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    width = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    geom = GeometryColumn(LineString(2))

GeometryDDL(Road.__table__)
