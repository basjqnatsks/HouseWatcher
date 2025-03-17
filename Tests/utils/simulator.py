from . import sql_postgre
import datetime
from . import yprices
from time import time
import pandas_market_calendars as mcal
from . import read
import json
import os
class simulate(object):
    def __new__(cls,Security,BuyDate,SellDate,sqlconn=None):
        cls.__init__(cls,Security,BuyDate,SellDate,sqlconn)
        return cls.RT
    def __init__(self,Security,BuyDate,SellDate,sqlconn) -> None:
        if not sqlconn:
            self.DB = sql_postgre.SQLP("house")
        else:
            self.DB = sqlconn
        if len(self.DB.Query(f"select 1 from public.simulator where ticker ='{Security}'")) == 0:
            raise IOError("No Ticker Found")
        
        self.Calender = self.DB.Query('select dateprice from public.marketcalender')
        for x in range(len(self.Calender)):
            self.Calender[x] = self.Calender[x][0]
        if type(BuyDate) == str:
            try:
                BuyDate = datetime.datetime.strptime(BuyDate, '%m-%d-%Y')
                BuyDateOfWeek = BuyDate.weekday()
            except ValueError:
                BuyDate = datetime.datetime.strptime(BuyDate, '%Y-%m-%d')
                BuyDateOfWeek = BuyDate.weekday()
        elif type(BuyDate) == datetime.datetime:
            BuyDateOfWeek = BuyDate.weekday()
        if type(SellDate) == str:
            try:
                SellDate = datetime.datetime.strptime(SellDate, '%m-%d-%Y')
                SellDateOfWeek = SellDate.weekday()
            except ValueError:
                SellDate = datetime.datetime.strptime(SellDate, '%Y-%m-%d')
                SellDateOfWeek = SellDate.weekday()
        elif type(SellDate) == datetime.datetime:
            SellDateOfWeek = SellDate.weekday()
        self.Today = datetime.datetime.today()
        try:
            BuyPrice = self.GetBuyPrice(self,Security,BuyDate)
            SellPrice = self.GetSellPrice(self,Security,SellDate)
            self.RT = (SellPrice-BuyPrice, round(SellPrice/BuyPrice,9))
        except Exception as f:
            print(f)
            return
        if not sqlconn:
            self.DB.Close()    
    def GetLastMarketDay(self):
        Today = datetime.datetime.today().date()# - datetime.timedelta(days=1)
        #CalList= yprices().CalDateList
        while Today not in self.Calender:
            Today -= datetime.timedelta(days=1)
        return Today
    def GetRecentDate(self,Security) -> datetime.date:
        BuyQ = f"select distinct dateprice from simulator where ticker = '{Security}' order by dateprice desc limit 1"
        try:
            return self.DB.Query(BuyQ)[0][0]
        except:
            return datetime.datetime.strptime('1950-01-01', '%Y-%m-%d').date()
    def GetBuyPrice(self,Security,BuyDate):
        BuyQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice >= '{BuyDate}' and dateprice <= '{self.Today}' order by dateprice ASC limit 1"
        print(BuyQ)
        return float(self.DB.Query(BuyQ)[0][0].replace('$', ''))
    def GetSellPrice(self,Security,SellDate):
        SellQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice <= '{SellDate}'  and dateprice <= '{self.Today}' order by dateprice desc limit 1"
        #print(SellQ)
        return float(self.DB.Query(SellQ)[0][0].replace('$', ''))


    #def test(self, Security,BuyDate,SellDate,Amount):

        #return (SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2))


