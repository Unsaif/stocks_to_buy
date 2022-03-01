import pandas as pd

def alpaca_translation(df):
    tickers_to_purchase = []
    tickers_to_sell = []
    for i, entry in df.iterrows():
        ticker = entry["Ticker"]
        if not pd.isnull(ticker):
            if entry["Type"] == "P" and "call options" not in entry["Description"]:
                tickers_to_purchase.append(ticker)
            else:
                tickers_to_sell.append(ticker)
    return set(tickers_to_purchase), set(tickers_to_sell)