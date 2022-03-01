from pydantic import BaseModel

class Trade(BaseModel):
    id: int
    name: str
    type: str
    ticker: str
    date: str
    doc_id: str
