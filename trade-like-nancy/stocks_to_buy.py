import pandas as pd
from .database import SessionLocal
from . import models, schemas

def create(db: SessionLocal, trade: schemas.Trade):
    
    trade_data = trade.dict()
    trade_capture = models.Trade(**trade_data)
    db.add(trade_capture)
    db.commit()
    db.refresh(trade_capture)
    db.close()

def alpaca_translation(df, name, doc_id, date): #finds tickers to buy for alpaca
    tickers_to_purchase = []
    tickers_to_sell = []
    try: #initialisation 
        index = int(SessionLocal().query(models.Trade).order_by(models.Trade.id.desc()).first().id)
    except AttributeError: #if trades table is empty
        index = 0 
    for i, entry in df.iterrows():
        ticker = entry["Ticker"]
        if not pd.isnull(ticker):
            #manual increment because errors caused when id: 0
            body = {"id": (index+1) + i, "name": name, "type": entry["Type"], "ticker": ticker, "date": date, "doc_id": doc_id} 
            create(SessionLocal(), trade=schemas.Trade(**body)) #adding trade to database

            if entry["Type"] == "P" and "call options" not in entry["Description"]:
                tickers_to_purchase.append(ticker)
            else:
                tickers_to_sell.append(ticker)

    return set(tickers_to_purchase), set(tickers_to_sell)