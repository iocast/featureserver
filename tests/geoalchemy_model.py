from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy import GeometryColumn, LineString, GeometryDDL

engine = create_engine('postgres://michel@localhost/featureserver', echo=False)
session = sessionmaker(bind=engine)()
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

class Road(Base):
    __tablename__ = 'fs_alchemy_road'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    width = Column(Integer)
    geom = GeometryColumn(LineString(2))

GeometryDDL(Road.__table__)

