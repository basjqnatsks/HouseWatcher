from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import datetime
from time import time
import os
import yfinance as yf
import requests
# db = sql_postgre.SQLP("house")
# ticker = []
# for x in db.Query('select distinct asset from public.transactions'):
#     print(x)
#     if '[st]' in x[0]:
#         ticker.append(x[0].split('(')[1].split(')')[0])

# for x in ticker:
# #     Q = db.Query(f"select distinct 1 from public.simulator where ticker ='{x}'")
# #     if len(Q) == 0:
#         print(x)

# print(simulator.simulate('tsla','01-01-2024', '01-01-2025'))
class SimulateCongress:
    def __init__(self) -> None:
        self.DB = sql_postgre.SQLP("house")
        QueryLsit = []
        Wallet = {}
        Qstring = """
select  trantype,asset,transdate,lastname,statedistrict
from public.transactions
join financialdisclosure on filingid = docid
where asset not like 'PICTURE' and transdate <= notificationdate and trantype like 'p'
order by transdate asc
"""
        for x in self.DB.Query(Qstring):
            QueryLsit.append(x)
        for x in range(len(QueryLsit)):
            QueryLsit[x] = list(QueryLsit[x])
            #$print(QueryLsit[x])
            if '(' in QueryLsit[x][1]:
                try:
                    QueryLsit[x][1] = QueryLsit[x][1].split('(')[1].split(')')[0]
                except:
                    continue
            QueryLsit[x][3] = QueryLsit[x][3].lower()
            QueryLsit[x][3] += QueryLsit[x][4].lower()
            del QueryLsit[x][-1]
            Wallet[QueryLsit[x][-1]] = []

        for x in QueryLsit:
            # print([x[1], x[2]])
            Wallet[x[-1]].append([x[1], x[2]])


        avglist = {}
        for x in Wallet:
            #print(x)
            avglist[x] = []
            for y in range(len(Wallet[x])):
                try:
                    Wallet[x][y] = simulator.simulate(Wallet[x][y][0] , Wallet[x][y][1], Wallet[x][y][1]+datetime.timedelta(days=365*3), self.DB)
                    avglist[x].append(Wallet[x][y][1])
                except IOError as poer:
                    print(poer)
        with open('out.csv', 'w') as f:
            for pop in avglist:
                f.write(pop+',')
                for too in avglist[pop]:
                    f.write(str(too)+',')
                f.write('\n')
        print(avglist)


SimulateCongress()
