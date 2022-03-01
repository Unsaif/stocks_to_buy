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
def create(request: schemas.Trade, db: Session = Depends(get_db)):
    trade = models.Trade()
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade
