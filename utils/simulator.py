from . import sql_postgre
import datetime
from . import yprices
from time import time
import pandas_market_calendars as mcal

class simulate:
    def __init__(self,Security,BuyDate,SellDate,Amount,sqlconn=None,cal = None) -> None:
        if cal:
            self.cal = cal
        if not sqlconn:
            self.DB = sql_postgre.SQLP("house")
        else:
            self.DB = sqlconn
        if type(BuyDate) == str:
            BuyDateOfWeek = datetime.datetime.strptime(BuyDate, '%m-%d-%Y').weekday()
        if type(SellDate) == str:
            SellDateOfWeek = datetime.datetime.strptime(SellDate, '%m-%d-%Y').weekday()

        Today = datetime.datetime.today()
        MostRecentDate = self.GetRecentDate(Security)
        DaysOfWeek = [1,2,3,4,5]
        #connect
        #return
        #(Price Difference, Multiply, Total Amount)
        #PopulateRangePrice(Security,SellDate,Today)
        if MostRecentDate != self.GetLastMarketDay() and MostRecentDate < datetime.datetime.strptime(SellDate, '%m-%d-%Y').date():
            self.RT =  (0,1,0)
            #return
            print('not up dto date')
            MostRecentDatePlusOneDay = MostRecentDate + datetime.timedelta(days=1)
            yprices.yprices().PopulateRangePrice(Security,MostRecentDatePlusOneDay,Today.date())
        try:
            #get Buy
            BuyPrice = self.GetBuyPrice(Security,BuyDate)
            #get Close
            SellPrice = self.GetSellPrice(Security,SellDate)
            self.RT = (1,1,1)
            self.RT = (SellPrice-BuyPrice, round(SellPrice/BuyPrice,9), round(SellPrice/BuyPrice*Amount,2))
        except Exception as f:
            print(f)
            return
        #print((SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2)))
        #self.test(Security,BuyDate,SellDate,Amount)
        if not sqlconn:
            self.DB.Close()    
    def GetLastMarketDay(self):
        
        Today = datetime.datetime.today().date() - datetime.timedelta(days=1)
        
        #CalList= yprices().CalDateList
        
        while Today not in self.cal:
            Today -= datetime.timedelta(days=1)
        
        
        return Today

    def GetRecentDate(self,Security):
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


    #def test(self, Security,BuyDate,SellDate,Amount):

        #return (SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2))

class SimulateCongress:
    def GenerateCalender(self):
        # Create a calendar
        nyse = mcal.get_calendar('NASDAQ')

        # Show available calendars
        #print(mcal.get_calendar_names())
        early = nyse.schedule(start_date='1900-01-01', end_date='2100-01-01')
        self.CalDateList = []
        for x in early.iloc[:, 0].items():
            self.CalDateList.append(x[0].date())



    def __init__(self) -> None:
        self.GenerateCalender()
        self.DB = SQLP("house")
        QueryLsit = []
        Wallet = {}
        Qstring = """
select  trantype,asset,transdate,lastname,statedistrict
from public.transactions
join financialdisclosure on filingid = docid
where asset not like 'PICTURE' and asset like '%[st]%' and transdate <= notificationdate and trantype like 'p'
order by transdate asc
"""
        for x in self.DB.Query(Qstring):
            QueryLsit.append(x)


        for x in range(len(QueryLsit)):
            QueryLsit[x] = list(QueryLsit[x])
            QueryLsit[x][1] = QueryLsit[x][1].split('(')[1].split(')')[0]
            QueryLsit[x][3] += QueryLsit[x][4]
            del QueryLsit[x][-1]
            Wallet[QueryLsit[x][-1]] = []

        for x in QueryLsit:
            Wallet[x[-1]].append([x[1], x[2]])
        avglist = {}
        for x in Wallet:
            avglist[x] = []
            for y in range(len(Wallet[x])):
                try:
                    #print(cal)
                    Wallet[x][y] = simulate(Wallet[x][y][0] , Wallet[x][y][1], '03-31-2024',1000, self.DB, self.CalDateList).RT
                    avglist[x].append(Wallet[x][y][1])
                    
                except:
                    pass
                print(y)
        with open('out.csv', 'w') as f:
            for pop in avglist:
                f.write(pop+',')
                for too in avglist[pop]:
                    f.write(str(too)+',')
                f.write('\n')
        print(avglist)

#simulate('intc', '01-01-2000', '04-01-2024',1000)
        


