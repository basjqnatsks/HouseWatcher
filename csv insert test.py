import psycopg2
from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import datetime
from time import time
import os
import yfinance as yf
import requests
import pathlib
from utils import calender,read
import os 
from time import time
from utils import sql_postgre 
from utils import read
import json
import datetime
import pathlib



def copy_csv_to_table():
    connection = psycopg2.connect(database='house', user="postgres", password="pass", host="localhost", port=5432)
    try:
        with connection, connection.cursor() as cur:
            sql = f"COPY simulator FROM STDIN WITH CSV HEADER"
            with open('combined.csv', 'r', encoding='utf-8') as f:
                cur.copy_expert(sql, f)

    except Exception as e:

        print("Error while copying data:", str(e))
    finally:
        connection.close()




with open('combined.csv','w') as f:
    f.write('dateprice,openprice,highprice,lowprice,closeprice,adjprice,volume,database,ticker,investmenttype\n')
    for zttt in os.walk(str(pathlib.Path(__file__).parent.resolve()) + "\\temp"):
        for z in zttt[2]:
            if 'yf_' in z:
                Ticker = z.replace('.csv', '').replace('yf_', '')
                var = read.read(str(pathlib.Path(__file__).parent.resolve()) + "\\temp\\" + z, '\n')
                del var[0]
                del var[0]
                del var[0]
                for y in range(len(var)):
                    var[y] = var[y].split(',')
                    try:
                        f.write(f"{var[y][0]},{var[y][4]},{var[y][2]},{var[y][3]},{var[y][1]},0,{var[y][5]},YF,{str(Ticker).lower()},equity\n")
                    except:
                        pass
            elif 'investing_' in z:
                Ticker = z.replace('.tmp', '').replace('investing_', '')
                try:
                    jsun = json.loads(read.read(str(pathlib.Path(__file__).parent.resolve()) + "\\temp\\" + z))
                except Exception as fp:
                    print(fp)
                else:
                    if not jsun['data']:
                        continue
                    for y in jsun['data']:
                        DatePrice =  y['rowDateTimestamp']
                        Open =  y['last_openRaw']
                        High = y['last_maxRaw']
                        Low = y['last_minRaw']
                        Close =  y['last_closeRaw']
                        volume = y['volumeRaw']
                        try:
                            f.write(f"{DatePrice},{Open},{High},{Low},{Close},0,{volume},INV,{z.split('_')[1]},None\n")
                            # DB.Insert('simulator', f"'{DatePrice}',{Open},{High},{Low},{Close},0,{volume},'INV', '{str(x[-1]).lower()}', '{z.replace('.csv','')}'")
                        except:
                            break

copy_csv_to_table()
