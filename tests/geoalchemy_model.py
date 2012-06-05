from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy import GeometryColumn, LineString, GeometryDDL

engine = create_engine('postgres://gis:gis@localhost/gis', echo=False)
session = sessionmaker(bind=engine)()
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

class Road(Base):
    __tablename__ = 'roads'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    width = Column(Integer)
    geom = GeometryColumn(LineString(2))

GeometryDDL(Road.__table__)

