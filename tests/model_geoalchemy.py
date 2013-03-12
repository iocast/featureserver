
from sqlalchemy import (create_engine, MetaData, Column, Integer, String, Unicode,
                        Numeric, func, literal, select)
from sqlalchemy.orm import sessionmaker, column_property
from sqlalchemy.ext.declarative import declarative_base

from pyspatialite import dbapi2 as sqlite
from geoalchemy import (Geometry, GeometryColumn, GeometryDDL,
                        WKTSpatialElement, Point)


engine = create_engine('sqlite://', module=sqlite, echo=False)

connection = engine.raw_connection().connection

metadata = MetaData(engine)
session = sessionmaker(bind=engine)()
#session.execute("SELECT InitSpatialMetaData()")
session.commit()

Base = declarative_base(metadata=metadata)

class FSPoint(Base):
    __tablename__ = 'fs_point'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    salary = Column(Integer)
    geom = GeometryColumn(Point(2))

GeometryDDL(FSPoint.__table__)

