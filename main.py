import sqlite3
import requests
import datetime
from io import BytesIO
from zipfile import ZipFile
import json
import xmltodict
class SQL:
    def __init__(self, dbname ) -> None:
        self.dbname = dbname
        self.connection = sqlite3.connect(self.dbname)

    def Refresh(self):
        self.connection.close()
        self.connection = sqlite3.connect(self.dbname)
    def ClearDB(self):
        for x in self.GetAllTables():
            tablename = x[0]
            self.connection.cursor().execute("drop table "+ str(tablename))
            self.Refresh()
    def CreateTables(self):
        self.connection.cursor().execute("CREATE TABLE movie(title, year, score)")
        self.connection.cursor().execute("CREATE TABLE FinancialDisclosure(FirstName, LastName, StateDistrict, FilingType, Year, FilingDate, DocID)")
        self.connection.cursor().execute("CREATE TABLE Transactions(FirstName, LastName, StateDistrict, TranType, Owner, Asset, Ticker, TransDate, FilingId,FilingDate,TradeDate,Amount,AmountLow,AmountHigh,NotificationDate)")
        self.Refresh()
    def PrintAllTables(self):
        print(self.GetAllTables())
    def GetAllTables(self):
        cur = self.connection.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        OUT =res.fetchall()
        self.Refresh()
        return OUT
    def Insert(self, table, values):
        __C = self.connection.cursor()
        
        __C.execute(f"INSERT INTO {table} VALUES ({values})")
        self.connection.commit()
        self.Refresh()
    def PrintAll(self, table):
        __C = self.connection.cursor()
        __C.execute(f"select * from " + table)
        for x in __C.fetchall():
            print(x)
    def SelectIfIn(self, table, column, data):
        __C = self.connection.cursor()
        print(f"select 1 from {table} where {column} = '{data}'")
        __C.execute(f"select 1 from {table} where {column} = '{data}'")#
        #select 1 from FinancialDisclosure where DocID = '8135688'
        print(__C.fetchone())
        self.Refresh()
    def Close(self):
        self.connection.close() 
    def Query(self, string):
        __C = self.connection.cursor()
        __C.execute(string)
        print(__C.fetchall())
class FinanceDisclosure:
    def __init__(self) -> None:
        self.FirstYear = 2008
        self.CurrentYear = int(datetime.date.today().year)
        self.URLS = []
        self.DB = SQL("HouseStockTrades.db")

        self.GenerateURLS()


        self.Run()
        self.DB.Close()
    @staticmethod
    def Url(Year: int) -> str:
        return f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{str(Year)}FD.zip'
    def GenerateURLS(self):
        #print( self.CurrentYear)
        for year in range(self.FirstYear, self.CurrentYear):
            #print(x)
            self.URLS.append(self.Url(year))
        #print(self.URLS)


    @staticmethod
    def Downloadfile(URL):
        return requests.get(URL)
    @staticmethod
    def UnzipBytes(byte):
        myzip = ZipFile(BytesIO(byte))
        return myzip
    @staticmethod
    def ReadzipFile(zip, filename):
        return zip.open(filename).read()
    @staticmethod
    def getZipFiles(zip):  
        return  zip.namelist()
    def printZipFiles(self, zip): 
        for x in self.getZipFiles(zip):
            print(x)


    def Run(self):
        self.DB.ClearDB()
        self.DB.CreateTables()
        for URL in self.URLS:
 
            BYTE = self.Downloadfile(URL).content
            ZIP = self.UnzipBytes(BYTE)
            FILENAME = None
            for Fn in self.getZipFiles(ZIP):
                if 'xml' in Fn.lower():
                    FILENAME = Fn
            
            if FILENAME:
                data = self.ReadzipFile(ZIP,FILENAME )
                dict = xmltodict.parse(data)
                
                Members = dict['FinancialDisclosure']['Member']
                for Member in Members:
                    self.DB.SelectIfIn('FinancialDisclosure', 'DocID', str(Member['DocID']))
                    self.DB.Insert('FinancialDisclosure', f"'{Member['First']}','{Member['Last']}','{Member['StateDst']}','{Member['FilingType']}','{Member['Year']}','{Member['FilingDate']}','{Member['DocID']}'")
                    #self.DB.Insert('movie', f"'tt','tt','tt'")
                    # print(x)
                    pass

            break

        #DB.PrintAllTables()


#SQL(sqlite3.connect("HouseStockTrades.db")).PrintAll('FinancialDisclosure')
#SQL("HouseStockTrades.db").Query("select 1 from FinancialDisclosure where DocID = '8216053'")
FC = FinanceDisclosure()

