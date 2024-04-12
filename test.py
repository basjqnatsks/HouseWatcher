from utils import simulator,sql_postgre
import pandas_market_calendars as mcal
import datetime
from time import time
import os
db = sql_postgre.SQLP("house")
t = time()
simulator.simulate('rick','2000-1-2','4-11-2024',1000, db)
print(str(time()-t))