from fastapi import FastAPI, Depends
from . import script
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from . import crud, models, schemas

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
    return stocks

@app.post('/trade')
async def create(request: schemas.Trade, db: Session = Depends(get_db)):
    trade = models.Trade(name=request.name, type=request.type, ticker=request.ticker, date=request.date, doc_id=request.doc_id)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

@app.get("/trades")
async def read_trades(db: Session = Depends(get_db)):
    trades = crud.get_trades(db)
    return trades

@app.post('/add_person')
async def create(request: schemas.People, db: Session = Depends(get_db)):
    person = models.People(last_name=request.last_name, first_name=request.first_name, last_doc_id=request.last_doc_id)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

