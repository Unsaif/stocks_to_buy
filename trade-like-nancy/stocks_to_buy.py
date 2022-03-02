import pandas as pd
import requests
from .database import SessionLocal
from . import models, schemas#, db=SessionLocal()

def create(db: SessionLocal, trade: schemas.Trade):
    trade_data = trade.dict()
    trade_capture = models.Trade(**trade_data)
    db.add(trade_capture)
    db.commit()
    db.refresh(trade_capture)
    #db.close()

def alpaca_translation(df, name, doc_id, date):
    tickers_to_purchase = []
    tickers_to_sell = []
    for i, entry in df.iterrows():
        ticker = entry["Ticker"]
        if not pd.isnull(ticker):
            if entry["Type"] == "P" and "call options" not in entry["Description"]:
                tickers_to_purchase.append(ticker)
            else:
                tickers_to_sell.append(ticker)
                
        body = {"id": 0, "name": name, "type": entry["Type"], "ticker": ticker, "date": date, "doc_id": doc_id}
        create(SessionLocal(), trade=schemas.Trade(**body))

    return set(tickers_to_purchase), set(tickers_to_sell)