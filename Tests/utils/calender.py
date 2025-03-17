from . import sql_postgre 
def getCalender() -> list:
    DB = sql_postgre.SQLP("house")
    Calender = DB.Query('select dateprice from public.marketcalender')
    for x in range(len(Calender)):
        Calender[x] = Calender[x][0]
    return Calender