from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import datetime
from time import time
import os
import yfinance as yf
import requests
from utils import calender,read
class ScrapeYfin:
    def __init__(self) -> None:
        self.Calender = calender.getCalender()
        self.Tickers = self.GetTickerList()
        self.Directory = 'temp\\'
        self.DB = sql_postgre.SQLP("house")
        hour = datetime.datetime.now().hour
        TodayDate = datetime.datetime.today().date()
        twentyonehundeDate = datetime.datetime.strptime('2100-01-01','%Y-%m-%d').date()
        for x in self.Tickers:
            Ticker = str(x[0].lower())
            print(Ticker)
            t= time()
            filename = f'temp/yf_{Ticker}.tmp'
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
                        try:
                            self.DB.Insert('simulator', f"'{var[y][0]}',{var[y][1]},{var[y][2]},{var[y][3]},{var[y][4]},{var[y][5]},{var[y][6]},'YF', '{Ticker}'")
                        except:
                            pass
    def GetLastMarketDay(self):
        Today = datetime.datetime.today().date()# - datetime.timedelta(days=1)
        #CalList= yprices().CalDateList
        while Today not in self.Calender:
            Today -= datetime.timedelta(days=1)
        return Today
    def GetTickerList(self):
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
    def UploadFileFromDisk(self,x):
        var  = read.read(self.Directory+ x, '\n')
        del var[0]
        
        for y in range(len(var)):
            var[y] = var[y].split(',')
            #print(var[y])
            if var[y] != [''] and datetime.datetime.strptime(var[y][0], '%Y-%m-%d').date() in self.Calender:
                #print('inserted')
                try:
                    self.DB.Insert('simulator', f"'{var[y][0]}',{var[y][1]},{var[y][2]},{var[y][3]},{var[y][4]},{var[y][5]},{var[y][6]},'YF', '{x.replace('.csv', '').replace('yf_', '')}'")
                except:
                    pass
ScrapeYfin()