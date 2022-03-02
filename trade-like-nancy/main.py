from fastapi import FastAPI, Depends
from . import script
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from . import models, schemas

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stocks_to_buy")
async def stocks_to_buy():
    stocks = script.script()
    print(stocks)
    return stocks

@app.post('/trade')
async def create(request: schemas.Trade, db: Session = Depends(get_db)):
    print(request)
    trade = models.Trade(name=request.name, type=request.type, ticker=request.ticker, date=request.date, doc_id=request.doc_id)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

