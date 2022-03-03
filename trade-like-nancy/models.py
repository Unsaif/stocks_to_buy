from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Trade(Base):

    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    ticker = Column(String)
    date = Column(Date)
    doc_id = Column(String)

class People(Base):

    __tablename__ = 'selected_individuals'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_name = Column(String)
    first_name = Column(String)
    last_doc_id = Column(String)