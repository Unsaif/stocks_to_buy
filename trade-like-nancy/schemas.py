from pydantic import BaseModel
import datetime

class Trade(BaseModel):
    id: int
    name: str
    type: str
    ticker: str
    date: datetime.date
    doc_id: str

class People(BaseModel):
    id: int
    last_name: str
    first_name: str
    last_doc_id: str
