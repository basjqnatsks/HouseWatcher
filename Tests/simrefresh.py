from utils import sql_postgre
import datetime
import os
from time import time
import pandas_market_calendars as mcal
from utils import read
from utils import yprices
import requests
class refresh:
    def __init__(self) -> None:
        self.DB = sql_postgre.SQLP("house")
        self.file = 'temp\\Calender.tmp'
        if not os.path.isfile(self.file):
            self.GenerateCalender()
        self.ReadCalender()
        self.ypricesz()
        #self.validatelinear('YF')
        
    def insertCalenderSQL(self):
        self.DB.Query("truncate public.marketcalender;")
        for x in self.Calender:
            self.DB.Query(f"INSERT INTO public.marketcalender VALUES ('{x}')")


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
    
    def ypricesz(self):

        
        Today = datetime.datetime.today()
        MostRecentDate = self.GetRecentDate(Security)
        LastMarketDay = self.GetLastMarketDay()
        DaysOfWeek = [1,2,3,4,5]
        if MostRecentDate != LastMarketDay and MostRecentDate < SellDate.date():
            MostRecentDatePlusOneDay = MostRecentDate + datetime.timedelta(days=1)



            yprices.yprices().PopulateRangePrice(Security,MostRecentDatePlusOneDay,'2100-01-01')
        yprices.yprices().PopulateAllPrices()
    # def validatelinear(self, db):    
    #     tickerlist = []
    #     for x in self.GetTickerList(db):
    #         tickerlist.append(x[0])

    #     for x in tickerlist:
    #         print(x)
    #         FloorDateDate = self.GetFloorDate(x, db)
    #         daterange = self.GetTickerDateRange(x,db)
    #         for alsl in range(len(daterange)):
    #             daterange[alsl] = daterange[alsl][0]
    #         if not self.__VAL(FloorDateDate, daterange):
    #             print(f'Error With {x} in db {db}')



    def validate(self, db):    
        tickerlist = []
        for x in self.GetTickerList(db):
            tickerlist.append(x[0])

        for x in tickerlist:
            print(x)
            FloorDateDate = self.GetFloorDate(x, db)
            daterange = self.GetTickerDateRange(x,db)
            for alsl in range(len(daterange)):
                daterange[alsl] = daterange[alsl][0]
            if not self.__VAL(FloorDateDate, daterange):
                print(f'Error With {x} in db {db}')

        #
    def ReadCalender(self):
        self.Calender = read.read(self.file, '\n')
        if len(self.Calender) < 1000:
            self.GenerateCalender()
            self.ReadCalender()
        for x in range(len(self.Calender)):
            self.Calender[x] = datetime.datetime.fromisoformat(self.Calender[x]).date()

    def __VAL(self, FloorDateDate, comparison):

        if FloorDateDate not in self.Calender:
            return False
        
        # for x in sel

        Today = self.Calender.index(FloorDateDate)
        #print(comparison[-1])
        while self.Calender[Today] <= comparison[-1]:
            if self.Calender[Today] not in comparison:
                return False
            Today +=1
        # print(self.Calender[Today])

        return True
    def GenerateCalender(self):
        nyse = mcal.get_calendar('NASDAQ')
        early = nyse.schedule(start_date='1900-01-01', end_date='2100-01-01')
        CalDateList = []
        for x in early.iloc[:, 0].items():
            CalDateList.append(x[0].date())
        with open(self.file, 'w') as f:
            for x in range(len(CalDateList)):
                #f.write(str(CalDateList[x].strftime('%Y-%m-%d')))
                f.write(str(CalDateList[x].isoformat()))
                if x != len(CalDateList)-1:
                    f.write('\n')


    def GetTickerDateRange(self,ticker, database: str) -> datetime.date:
        BuyQ = f"select distinct dateprice from simulator where ticker = '{ticker}' and database = '{database.upper()}' order by dateprice asc"
        return self.DB.Query(BuyQ)       
    def GetLastMarketDay(self):
        Today = datetime.datetime.today().date()# - datetime.timedelta(days=1)
        #CalList= yprices().CalDateList
        while Today not in self.Calender:
            Today -= datetime.timedelta(days=1)
        return Today
    def GetTickerList(self,database: str) -> datetime.date:
        BuyQ = f"select distinct ticker from simulator where database = '{database.upper()}'"
        return self.DB.Query(BuyQ)
    def GetFloorDate(self,Security,database: str) -> datetime.date:
        BuyQ = f"select distinct dateprice from simulator where ticker = '{Security}' and database = '{database.upper()}' order by dateprice asc limit 1"
        return self.DB.Query(BuyQ)[0][0]
    def GetRecentDate(self,Security,database) -> datetime.date:
        BuyQ = f"select distinct dateprice from simulator where ticker = '{Security}' order by dateprice desc limit 1"
        try:
            return self.DB.Query(BuyQ)[0][0]
        except:
            return datetime.datetime.strptime('1950-01-01', '%Y-%m-%d').date()
    def GetBuyPrice(self,Security,BuyDate):
        BuyQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice >= '{BuyDate}' order by dateprice ASC limit 1"
        return float(self.DB.Query(BuyQ)[0][0].replace('$', ''))
    def GetSellPrice(self,Security,SellDate):
        SellQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice <= '{SellDate}' order by dateprice desc limit 1"
        return float(self.DB.Query(SellQ)[0][0].replace('$', ''))



refresh()