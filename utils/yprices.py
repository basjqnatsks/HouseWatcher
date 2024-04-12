import yfinance as yf
from . import sql_postgre
from . import read
import os
import requests
import pandas_market_calendars as mcal
import datetime
from time import time
class yprices:
    def __init__(self, sqldbconn = None) -> None:
        self.Directory = 'yfinance\\'
        if not sqldbconn:
            self.DB = sql_postgre.SQLP("house")
        self.GenerateCalender()
        #self.UploadFromDisk()
        #self.PopulateAllPrices()

    def GenerateCalender(self):
        # Create a calendar
        nyse = mcal.get_calendar('NASDAQ')

        # Show available calendars
        #print(mcal.get_calendar_names())
        early = nyse.schedule(start_date='1900-01-01', end_date='2100-01-01')
        self.CalDateList = []
        for x in early.iloc[:, 0].items():
            self.CalDateList.append(x[0].date())


    def UploadFromDisk(self):
        for x in os.listdir(self.Directory):
            var  = read.read(self.Directory+ x, '\n')
            del var[0]
            
            for y in range(len(var)):
                var[y] = var[y].split(',')
                #print(var[y])
                if var[y] != [''] and datetime.datetime.strptime(var[y][0], '%Y-%m-%d').date() in self.CalDateList:
                    #print('inserted')
                    self.DB.Insert('simulator', f"'{var[y][0]}',{var[y][1]},{var[y][2]},{var[y][3]},{var[y][4]},{var[y][5]},{var[y][6]},'YF', '{x.replace('.csv', '')}'")

                #print(y)
    @staticmethod
    def DeleteFolder(dir):
        print('del')
        try:
            for x in os.listdir(dir):
                try:
                    os.remove(dir+x)
                except Exception as df:
                    pass
                    #print(df)
        except Exception as df:
            pass
            #print(df)
        try:
            os.mkdir(dir)
        except Exception as df:
            pass
            #print(df)


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
    
    def PopulateAllPrices(self):
        self.DeleteFolder(self.Directory)
        try:
            os.mkdir(self.Directory)
        except:
            pass
        self.TickerList = self.GetTickerList()
        for x in self.TickerList:
            try:
                yf.download( x[0], '1950-01-01', '2025-01-01').to_csv(f'{self.Directory}/{ x[0]}.csv')
            except Exception as f:
                print(f)

    def PopulateRangePrice(self,ticker, BeginRange, EndRange):

        self.DeleteFolder(self.Directory)
        try:
            os.mkdir(self.Directory)
        except:
            pass
        try:

            yf.download(ticker, BeginRange, EndRange).to_csv(f'{self.Directory}/{ ticker}.csv')
        except Exception as f:
            print(f)

        self.UploadFromDisk()

    # def __del__(self) -> None:
    #     self.DB.Close()