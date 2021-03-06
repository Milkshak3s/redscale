from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Target(Base):
    __tablename__ = 'targets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    last_active = Column(Integer)
