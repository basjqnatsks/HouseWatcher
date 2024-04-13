from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import datetime
from time import time
import os
import yfinance as yf
import requests
db = sql_postgre.SQLP("house")
t = time()
simulator.simulate('tsla','2000-1-2','3-11-2024',1000, db)
print(str(time()-t))

yf.download('twtr', '01-01-2020', '01-01-2021').to_csv(f'34334.csv')

def GetTickerList():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',

        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.sec.gov/include/ticker.txt', headers=headers)
    TICKER_LIST = str(response.text)
    TICKER_LIST = TICKER_LIST.split('\n')
    for x in range(len(TICKER_LIST)):
        TICKER_LIST[x] = TICKER_LIST[x].split('\t')
    return TICKER_LIST

ff = GetTickerList()
