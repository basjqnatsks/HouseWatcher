from sql_postgre import SQLP
import datetime
from yprices import yprices
class simulate:



    def __init__(self,Security,BuyDate,SellDate,Amount) -> None:
        BuyDateOfWeek = datetime.datetime.strptime(BuyDate, '%m-%d-%Y').weekday()
        SellDateOfWeek = datetime.datetime.strptime(SellDate, '%m-%d-%Y').weekday()
        Today = datetime.datetime.today()


        DaysOfWeek = [1,2,3,4,5]
        #connect
        self.DB = SQLP("house")
        #get Buy
        BuyPrice = self.GetBuyPrice(Security,BuyDate)

        #get Close
        SellPrice = self.GetSellPrice(Security,SellDate)
        #return

        #(Price Difference, Multiply, Total Amount)
        #PopulateRangePrice(Security,SellDate,Today)
        MostRecentDate = self.GetRecentDate(Security)

        if MostRecentDate != self.GetLastMarketDay():
            MostRecentDatePlusOneDay = MostRecentDate + datetime.timedelta(days=1)
            yprices().PopulateRangePrice(Security,MostRecentDatePlusOneDay,Today.date())
        print((SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2)))
        #self.test(Security,BuyDate,SellDate,Amount)
        self.DB.Close()
        

    def GetLastMarketDay(self):
        Today = datetime.datetime.today().date() - datetime.timedelta(days=1)
        CalList= yprices().CalDateList
        while Today not in CalList:
            Today -= datetime.timedelta(days=1)

        return Today

    def GetRecentDate(self,Security):
        BuyQ = f"select distinct dateprice from simulator where ticker = '{Security}' order by dateprice desc limit 1"
        return self.DB.Query(BuyQ)[0][0]

    def GetBuyPrice(self,Security,BuyDate):
        BuyQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice >= '{BuyDate}' order by dateprice ASC limit 1"
        return float(self.DB.Query(BuyQ)[0][0].replace('$', ''))
    def GetSellPrice(self,Security,SellDate):
        SellQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice <= '{SellDate}' order by dateprice desc limit 1"
        return float(self.DB.Query(SellQ)[0][0].replace('$', ''))


    #def test(self, Security,BuyDate,SellDate,Amount):

        #return (SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2))

simulate('msft', '01-01-2010', '03-30-2024',1000)