from . import stocks_to_buy
from . import get_trading_dataframes
from .database import SessionLocal, engine
from . import models

import zipfile
import requests
import os
import pandas as pd
from datetime import date

def script():

    people = SessionLocal().query(models.People) #Retrieve people of interest
    people_df = pd.read_sql(people.statement, engine) 

    todays_date = date.today()

    #todays_date_formatted = todays_date.strftime("%d/%m/%y")
    
    # fetching the current year
    year = todays_date.year

    zip_file_url=f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.ZIP" 
    pdf_file_url=f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/"
    r=requests.get(zip_file_url)
    zipfile_name = f'zip_extraction/{year}.zip'

    with open(zipfile_name, 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(zipfile_name) as z:
        z.extractall('zip_extraction')

    financial_disclosure_df = pd.read_csv(f"zip_extraction/{year}FD.txt", sep="\t")
    financial_disclosure_df['FilingDate'] = pd.to_datetime(financial_disclosure_df['FilingDate'])

    #retrieve dataframes that contain new trades by people of interest
    trading_dataframes = get_trading_dataframes.gettradingdataframes(financial_disclosure_df, people_df, pdf_file_url)

    dirs = ['pdfs', 'zip_extraction'] #delete all files except .gitkeep in folders
    for dir in dirs:
        for f in os.listdir(dir):
            if f == ".gitkeep":
                continue
            else:
                os.remove(os.path.join(dir, f))

    stocks = []
    for key in trading_dataframes:
        first_name = people_df[people_df["last_name"] == key]["first_name"][0]
        new_doc_id = people_df[people_df["last_name"] == key]["last_doc_id"][0]
        name = f"{first_name} {key}"
        tickers_to_buy, tickers_to_sell = stocks_to_buy.alpaca_translation(trading_dataframes[key], name, new_doc_id, todays_date)
        ticker_string = ", ".join(tickers_to_buy)
        if len(tickers_to_buy) != 0:
            print(f"{key} purchased: {ticker_string}\n")
            for ticker in tickers_to_buy:
                stocks.append(ticker)

    stocks = list(set(stocks))

    return stocks