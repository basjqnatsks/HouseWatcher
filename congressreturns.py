from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import datetime

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
    @staticmethod
    def to_csv (Stream: open, Iterator: list):
        with Stream as f:
            for pop in Iterator:
                f.write(pop+',')
                for too in Iterator[pop]:
                    f.write(str(too)+',')
                f.write('\n')
    def Method2(self) -> None:
        self.GenerateCalender()
        self.DB = sql_postgre.SQLP("house")
        QueryLsit = []
        Wallet = {}
        DateList = []
        DatesString = """
select  distinct transdate
from public.transactions
join financialdisclosure on filingid = docid
where asset not like 'PICTURE' and asset like '%[st]%' and transdate <= notificationdate and trantype like 'p'
order by transdate asc
"""
        for x in self.DB.Query(DatesString):
            DateList.append(x)


        for x in DateList:

            
            Qstring = f"""
    select  trantype,asset,transdate,lastname,statedistrict
    from public.transactions
    join financialdisclosure on filingid = docid
    where asset not like 'PICTURE' and asset like '%[st]%' and transdate <= notificationdate and trantype like 'p' and transdate = '{x[0].strftime('%Y-%m-%d')}'
    order by transdate asc
    """
            print(Qstring)
            for  y in self.DB.Query(Qstring):
                print(y)
        return
        for x in self.DB.Query(Qstring):
            QueryLsit.append(x)


        Percent = 1.0
        print(DateList)
        for x in QueryLsit:
            print(x)

        return




        for x in Wallet:
            avglist[x] = []
            for y in range(len(Wallet[x])):
                try:
                    #print(cal)
                    Wallet[x][y] = simulator.simulate(Wallet[x][y][0] , Wallet[x][y][1], '03-31-2024',1000, self.DB, self.CalDateList).RT
                    avglist[x].append(Wallet[x][y][1])
                    
                except:
                    pass
                print(y)

        print(avglist)


    def Method1(self) -> None:
        self.GenerateCalender()
        self.DB = sql_postgre.SQLP("house")
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
                    Wallet[x][y] = simulator.simulate(Wallet[x][y][0] , Wallet[x][y][1], '03-31-2024',1000, self.DB, self.CalDateList).RT
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




SimulateCongress().Method2()