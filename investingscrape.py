import os 
from time import time
from utils import sql_postgre 
from utils import read
import json
import datetime
import pathlib
DB = sql_postgre.SQLP("house")
Calender = DB.Query('select dateprice from public.marketcalender')
for x in range(len(Calender)):
    Calender[x] = Calender[x][0]


def GetLastMarketDay():
    Today = datetime.datetime.today().date()# - datetime.timedelta(days=1)
    #CalList= yprices().CalDateList

    while Today not in Calender:
        Today -= datetime.timedelta(days=1)
    return Today
finalList = []
d = read.read(str(pathlib.Path(__file__).parent.resolve()) + '\\investing_stocks.csv', '\n')
for x in range(len(d)):
    d[x] = d[x].split(',')
    if d[x][0] == 'united states':
        finalList.append(d[x])

for x in finalList:
    try:
        int(x[-3])
    except:
        print(x)
    else:
        t= time()
        filename = str(pathlib.Path(__file__).parent.resolve()) + f'\\temp\\investing_{str(x[-1])}_{str(x[-3])}.tmp'
        ticker = str(x[-1]).lower()
        print(ticker)
        query = DB.Query(f"select dateprice from simulator where ticker = '{ticker}' and database  = 'INV' order by dateprice desc limit 1")
        if len(query) > 0:
            MostUpToDate = query[0][0]
            MarketDateToday = GetLastMarketDay()
            print(MarketDateToday)
            if MarketDateToday != MostUpToDate:
                if MostUpToDate == datetime.datetime.strptime('2100-01-01','%Y-%m-%d').date():
                    continue

                if MarketDateToday - datetime.timedelta(days=1) == MostUpToDate and datetime.datetime.now().hour >= 18:
                    os.system(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date={MarketDateToday}&end-date=2100-01-01&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --output {filename}')   
                elif MarketDateToday - datetime.timedelta(days=1) == MostUpToDate and datetime.datetime.now().hour < 17:
                    continue
                else:
                    #print(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date={query[0][0] + datetime.timedelta(days=1)}&end-date=2100-01-01&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --Output {filename}')
                    os.system(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date={query[0][0] + datetime.timedelta(days=1)}&end-date=2100-01-01&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --output {filename}')
            else:
                continue
        else:
            os.system(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date=1995-01-01&end-date=2100-01-01&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --output {filename}')
        try:
            jsun = json.loads(read.read(filename))
        except Exception as fp:
            print(fp)
        else:
            if not jsun['data']:
                DB.Insert('simulator', f"'2100-01-01',-1,-1,-1,-1,0,-1,'INV', '{str(x[-1]).lower()}'")
                continue
            for y in jsun['data']:
                DatePrice =  y['rowDateTimestamp']
                Open =  y['last_openRaw']
                High = y['last_maxRaw']
                Low = y['last_minRaw']
                Close =  y['last_closeRaw']
                volume = y['volumeRaw']
                try:
                    DB.Insert('simulator', f"'{DatePrice}',{Open},{High},{Low},{Close},0,{volume},'INV', '{str(x[-1]).lower()}'")
                except:
                    break
print(len(finalList))       