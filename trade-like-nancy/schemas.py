from pydantic import BaseModel
import datetime

class Trade(BaseModel):
    id: int
    name: str
    type: str
    ticker: str
    date: datetime.date
    doc_id: str
