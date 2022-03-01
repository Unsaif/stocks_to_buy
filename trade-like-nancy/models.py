from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Trade(Base):

    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    ticker = Column(String)
    date = Column(Date)
    doc_id = Column(String)