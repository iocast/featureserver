from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy import GeometryColumn, LineString, GeometryDDL, Point

engine = create_engine('postgres://michel@localhost/featureserver', echo=False)
session = sessionmaker(bind=engine)()
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

class Road(Base):
    __tablename__ = 'fs_point'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    geom = GeometryColumn(Point(2))

GeometryDDL(Road.__table__)

