import pandas as pd

from twstock import __update_codes as tw__update_codes
tw__update_codes()
from twstock import Stock
# twstock.__update_codes()
# import yfinance as yf

from includes.vs_modules.calculate_kd_index import calculateKDIndex

def get_stock_data_31day(code:str) -> pd.DataFrame:
    # stock = yf.Ticker(code)
    # hist = stock.history(period="1mo")
    stock = Stock(code)
    df = pd.DataFrame(stock.fetch_31())
    df = calculateKDIndex(df).set_index("date")
    # print(df)
    # df = calculateKDIndex(hist)
    return df
    # return df.to_json()