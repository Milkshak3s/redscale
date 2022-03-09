from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, TEXT, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Command(Base):
    __tablename__ = 'commands'
    
    id = Column(Integer, primary_key=True)
    target = Column(Integer)
    command = Column(TEXT(16383))
    pending = Column(BOOLEAN)
