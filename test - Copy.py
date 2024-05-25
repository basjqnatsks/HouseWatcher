from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import requests
from time import time

import yfinance as yf

import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.sec.gov/file/company-tickers',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    '^sec-ch-ua-platform': '^\\^Windows^\\^^',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}
DB = sql_postgre.SQLP("house")
response = requests.get('https://www.sec.gov/files/company_tickers.json', headers=headers)
jsonstuff = response.json()
DoesExist = []
for x in DB.Query("select distinct ticker from simulator where dateprice = '2100-01-01'"):
    if x[0] in jsonstuff:
        DoesExist.append(x[0])


print(DoesExist)