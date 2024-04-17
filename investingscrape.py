import os 
from time import time
from utils import sql_postgre 
from utils import read
import json
finalList = []
d = read.read('investing_stocks.csv', '\n')
for x in range(len(d)):
    d[x] = d[x].split(',')
    if d[x][0] == 'united states':
        finalList.append(d[x])


DB = sql_postgre.SQLP("house")
for x in finalList:
    try:
        int(x[-3])
    except:
        print(x)
    else:
        t= time()
        filename = f'temp/investing_{str(x[-1])}_{str(x[-3])}.tmp'
        ticker = str(x[-1]).lower()
        print(ticker)
        #print(len(DB.Query(f"select * from simulator where ticker = 'ba' and database  = 'INV' limit 1")))
        query = DB.Query(f"select dateprice from simulator where ticker = '{ticker}' and database  = 'INV' order by dateprice desc limit 1")

        if len(query) > 0:
            print(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date={query[0][0]}&end-date=2100-01-01&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --Output {filename}')
            os.system(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date={query[0][0]}&end-date=2100-01-01&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --Output {filename}')
            #print('skipping')
        else:
        #print(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date=2005-01-01&end-date=2030-04-13&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --Output {filename}')
            os.system(f'curl "https://api.investing.com/api/financialdata/historical/{str(x[-3])}?start-date=1995-01-01&end-date=2100-01-01&time-frame=Daily&add-missing-rows=false" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0" -H "Accept: application/json, text/plain, */*" -H "Origin: https://www.investing.com" -H "domain-id: www" --Output {filename}')
        try:
            jsun = json.loads(read.read(filename))
        except Exception as fp:
            print(fp)
        else:

            for y in jsun['data']:
                DatePrice =  y['rowDateTimestamp']
                Open =  y['last_openRaw']
                High = y['last_maxRaw']
                Low = y['last_minRaw']
                Close =  y['last_closeRaw']
                volume = y['volumeRaw']
                
                #print('simulator', f"'{DatePrice}',{Open},{High},{Low},{Close},0,{volume},'INV', '{str(x[-1])}'")
                try:
                    DB.Insert('simulator', f"'{DatePrice}',{Open},{High},{Low},{Close},0,{volume},'INV', '{str(x[-1]).lower()}'")
                except:
                    break
                #os.remove(filename)
        #print(time()-t)
    #break
print(len(finalList))       