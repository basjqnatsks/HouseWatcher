from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import datetime
from time import time
import os
import yfinance as yf
import requests
import pathlib
from utils import calender,read
class ScrapeYfin:
    def __init__(self) -> None:
        
        self.Calender = calender.getCalender()
        self.Tickers = self.GetTickerList()
        self.Directory = str(pathlib.Path(__file__).parent.resolve()) + '\\temp\\'
        self.DB = sql_postgre.SQLP("house")
        hour = datetime.datetime.now().hour
        TodayDate = datetime.datetime.today().date()
        twentyonehundeDate = datetime.datetime.strptime('2100-01-01','%Y-%m-%d').date()
        for x in self.Tickers:
            Ticker = str(x[0].lower())
            print(Ticker)
            t= time()
            filename = str(pathlib.Path(__file__).parent.resolve()) + f'\\temp\\yf_{Ticker}.tmp'

            query = self.DB.Query(f"select dateprice from simulator where ticker = '{Ticker}' and database  = 'YF' order by dateprice desc limit 1")
            if len(query) > 0:
                MostUpToDate = query[0][0]
                MarketDateToday = self.GetLastMarketDay()
                if MarketDateToday != MostUpToDate:
                    if MostUpToDate == twentyonehundeDate:
                        continue 
                    if MarketDateToday - datetime.timedelta(days=1) == MostUpToDate and TodayDate == MarketDateToday and hour >= 18:
                        yf.download(Ticker, MarketDateToday, '2050-01-01').to_csv(filename)
                        
                    elif MarketDateToday - datetime.timedelta(days=1) == MostUpToDate and TodayDate == MarketDateToday and hour < 17:
                        continue
                    elif MarketDateToday - datetime.timedelta(days=1) == MostUpToDate and TodayDate != MarketDateToday:
                        yf.download(Ticker, MarketDateToday, '2050-01-01').to_csv(filename)

                    else:
                        yf.download(Ticker, MostUpToDate + datetime.timedelta(days=1), '2050-01-01').to_csv(filename)
                else:
                    continue
            else:
                print(Ticker)
                yf.download(Ticker, '1950-01-01', '2050-01-01').to_csv(filename)
            try:
                var  = read.read(filename, '\n')
                del var[0]
            except Exception as fp:
                print(fp)
            else:
                if var == ['']:
                    self.DB.Insert('simulator', f"'2100-01-01',-1,-1,-1,-1,0,-1,'YF', '{Ticker}'")
                    continue      
                for y in range(len(var)):
                    var[y] = var[y].split(',')
                    if var[y] != ['']:
                        # print('simulator', f"'{var[y][0]}',{var[y][4]},{var[y][2]},{var[y][3]},{var[y][1]},0,{var[y][5]},'YF', '{str(x[-1]).lower()}'")
                        # self.DB.Insert('simulator', f"'{var[y][0]}',{var[y][4]},{var[y][2]},{var[y][3]},{var[y][1]},0,{var[y][5]},'YF', '{str(Ticker).lower()}'")
                        try:
                            self.DB.Insert('simulator', f"'{var[y][0]}',{var[y][4]},{var[y][2]},{var[y][3]},{var[y][1]},0,{var[y][5]},'YF', '{str(Ticker).lower()}','equity'")
                        except Exception as a:
                            pass
                            # print(a)
            # break
    def GetLastMarketDay(self):
        Today = datetime.datetime.today().date()# - datetime.timedelta(days=1)
        #CalList= yprices().CalDateList
        while Today not in self.Calender:
            Today -= datetime.timedelta(days=1)
        return Today
    def GetTickerList(self):
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
    'Priority': 'u=0, i',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
      }
        response = requests.get('https://www.sec.gov/include/ticker.txt', headers=headers)
        open('test.html', 'wb').write(response.content)
        TICKER_LIST = str(response.text)
        TICKER_LIST = TICKER_LIST.split('\n')
        for x in range(len(TICKER_LIST)):
            TICKER_LIST[x] = TICKER_LIST[x].split('\t')
        return TICKER_LIST

ScrapeYfin()