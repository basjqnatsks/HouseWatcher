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

    def Method3(self) -> None:
        f = open('out.csv', 'w')
        self.GenerateCalender()
        self.DB = sql_postgre.SQLP("house")
        QueryLsit = []
        Wallet = {}
        DateList = []
        DatesString = """
select  distinct transdate
from public.transactions
join financialdisclosure on filingid = docid
where asset not like 'PICTURE' 

and transdate <= notificationdate 
and trantype like 'p'
order by transdate asc
"""
        for x in self.DB.Query(DatesString):
            DateList.append(x)
        amount = 1000
        for x in range(len(DateList)):
            Qstring = f"""
    select  trantype,asset,transdate,financialdisclosure.lastname,financialdisclosure.statedistrict
    from public.transactions
    join financialdisclosure on filingid = docid
    where asset not like 'PICTURE' 
    and transdate <= notificationdate 
    and trantype like 'p' and transdate = '{DateList[x][0].strftime('%Y-%m-%d')}'
    order by transdate asc
    """
            #print(Qstring)
            TMPARR =  self.DB.Query(Qstring)
            avgpercentage = 0
            avgcount = 0
            for  y in range(len(TMPARR)):
                #print(y)
                try:
                    date = DateList[x+1][0].strftime('%m-%d-%Y')
                except Exception as e:
                    #print(e)
                    date = datetime.date.today().strftime('%m-%d-%Y')
                print(TMPARR[y][1])
                try:
                    ticker = TMPARR[y][1].split('(')[1].split(')')[0]
                except:
                    continue
                buydate = TMPARR[y][2].strftime('%m-%d-%Y')
                lastname = TMPARR[y][3]
                statedistrict = TMPARR[y][4]
                try:
                    simobj = simulator.simulate(ticker,buydate,'3-17-2025',self.DB,self.CalDateList)
                    f.write(f"{ticker},{buydate},{str(simobj[1])},{'3-17-2025'},{lastname},{statedistrict}\n")

                except:
                    pass

        return





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

        amount = 1000
        for x in range(len(DateList)):

            
            Qstring = f"""
    select  trantype,asset,transdate,financialdisclosure.lastname,financialdisclosure.statedistrict
    from public.transactions
    join financialdisclosure on filingid = docid
    where asset not like 'PICTURE' and asset like '%[st]%' and transdate <= notificationdate and trantype like 'p' and transdate = '{DateList[x][0].strftime('%Y-%m-%d')}'
    order by transdate asc
    """
            #print(Qstring)
            TMPARR =  self.DB.Query(Qstring)
            avgpercentage = 0
            avgcount = 0
            for  y in range(len(TMPARR)):
                #print(y)
                try:
                    date = DateList[x+1][0].strftime('%m-%d-%Y')
                except Exception as e:
                    #print(e)
                    date = datetime.date.today().strftime('%m-%d-%Y')
                ticker = TMPARR[y][1].split('(')[1].split(')')[0]
                buydate = TMPARR[y][2].strftime('%m-%d-%Y')
                print(ticker)
                try:
                    simobj = simulator.simulate(ticker,buydate,date,self.DB,self.CalDateList)
                    print(simobj)
                except:
                    continue
                try:
                    avgpercentage += simobj.RT[1]
                    avgcount += 1
                except:
                    pass
            if avgcount > 0:
                amount *= round(avgpercentage / avgcount, 9)
                print(amount)
                print(DateList[x][0].strftime('%Y-%m-%d') + ': ' + str(amount))
                #print(round(avgpercentage / avgcount, 9))
                #print(simobj.RT)
            
                #print(simulator.simulate(TMPARR[y][1].split('(')[1].split(')')[0] , TMPARR[y][2].strftime('%m-%d-%Y'), date ,1000, self.DB, self.CalDateList).RT[1])
                #break
        return



    def Method1(self) -> None:
        self.GenerateCalender()
        self.DB = sql_postgre.SQLP("house")
        QueryLsit = []
        Wallet = {}
        Qstring = """
select  trantype,asset,transdate,financialdisclosure.lastname,financialdisclosure.statedistrict
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
                # try:
                #     #print(cal)
                Wallet[x][y] = simulator.simulate(Wallet[x][y][0] , Wallet[x][y][1], '03-31-2024', self.DB, self.CalDateList)
                print( simulator.simulate(Wallet[x][y][0] , Wallet[x][y][1], '03-31-2024', self.DB, self.CalDateList))
                avglist[x].append(Wallet[x][y][1])

                    
                # except :
                #     pass
                print(y)
        with open('out.csv', 'w') as f:
            for pop in avglist:
                f.write(pop+',')
                for too in avglist[pop]:
                    f.write(str(too)+',')
                f.write('\n')
        print(avglist)




SimulateCongress().Method3()