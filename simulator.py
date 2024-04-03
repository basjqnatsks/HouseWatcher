from sql_postgre import SQLP
import datetime
from yprices import yprices
class simulate:



    def __init__(self,Security,BuyDate,SellDate,Amount,sqlconn=None) -> None:
        if not sqlconn:
            self.DB = SQLP("house")
        else:
            self.DB = sqlconn
        if type(BuyDate) == str:
            BuyDateOfWeek = datetime.datetime.strptime(BuyDate, '%m-%d-%Y').weekday()
        SellDateOfWeek = datetime.datetime.strptime(SellDate, '%m-%d-%Y').weekday()
        Today = datetime.datetime.today()
        MostRecentDate = self.GetRecentDate(Security)

        DaysOfWeek = [1,2,3,4,5]
        #connect
        

        #return

        #(Price Difference, Multiply, Total Amount)
        #PopulateRangePrice(Security,SellDate,Today)

    
        print(MostRecentDate)
        if MostRecentDate != self.GetLastMarketDay() and MostRecentDate < datetime.datetime.strptime(SellDate, '%m-%d-%Y').date():
            print('not up dto date')
            MostRecentDatePlusOneDay = MostRecentDate + datetime.timedelta(days=1)
            yprices().PopulateRangePrice(Security,MostRecentDatePlusOneDay,Today.date())


        #get Buy
        BuyPrice = self.GetBuyPrice(Security,BuyDate)

        #get Close
        SellPrice = self.GetSellPrice(Security,SellDate)



        print((SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2)))
        #self.test(Security,BuyDate,SellDate,Amount)


        if not sqlconn:
            self.DB.Close()
        

    def GetLastMarketDay(self):
        Today = datetime.datetime.today().date() - datetime.timedelta(days=1)
        CalList= yprices().CalDateList
        while Today not in CalList:
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
    
    def __init__(self) -> None:
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
                    Wallet[x][y] = simulate(Wallet[x][y][0] , Wallet[x][y][1], '03-31-2024',1000, self.DB)
                    avglist[x].append(Wallet[x][y][1])
                     
                except:
                    pass
                print(y)
        
        
        print(Wallet)



        









    def __del__(self) -> None:
        self.DB.Close()




SimulateCongress()
#simulate('intc', '01-01-2000', '04-01-2024',1000)