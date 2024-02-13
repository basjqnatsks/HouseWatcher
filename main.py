import sqlite3
import requests
import datetime
from io import BytesIO
from zipfile import ZipFile
import json
import xmltodict
from lxml import etree
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
        #self.Refresh()
    def PrintAll(self, table):
        __C = self.connection.cursor()
        __C.execute(f"select * from " + table)
        for x in __C.fetchall():
            print(x)
    def SelectIfIn(self, table, column, data):
        __C = self.connection.cursor()
        #print(f"select 1 from {table} where {column} = '{data}'")
        __C.execute(f"select 1 from {table} where {column} = '{data}'")#
        #select 1 from FinancialDisclosure where DocID = '8135688'
        _T_ =  __C.fetchone()
        self.Refresh()
        try:
            _T_[0]
        except:
            return 0
        else:
            return _T_[0]
    def Close(self):
        self.connection.close() 
    def Query(self, string):
        __C = self.connection.cursor()
        __C.execute(string)
        self.connection.commit()
        return __C.fetchall()
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
        DoesExist = []
        for x in self.DB.Query('select distinct year from FinancialDisclosure'):
            DoesExist.append(x[0])
        print(DoesExist)
        for year in range(self.FirstYear, self.CurrentYear+1):
            #print(self.CurrentYear-2)
            if str(year) not in DoesExist or year > self.CurrentYear-2:
                print(year)
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
    @staticmethod
    def CleanMember(StringDict):
        for x in StringDict:
            try:
                StringDict[x] = StringDict[x].replace('"','').replace("'",'')
            except:
                pass


    def Run(self):
        #self.DB.ClearDB()
        #self.DB.CreateTables()
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
                DoesExist = []
                for x in self.DB.Query('Select Distinct DocId from FinancialDisclosure'):
                    DoesExist.append(x[0])
                #print(DoesExist)
                Members = dict['FinancialDisclosure']['Member']
                for Member in Members:
                    
                    if Member['DocID'] not in DoesExist:
                        
                        self.CleanMember(Member)
                        #print(Member)
                        self.DB.Insert('FinancialDisclosure', f"'{Member['First']}','{Member['Last']}','{Member['StateDst']}','{Member['FilingType']}','{Member['Year']}','{Member['FilingDate']}','{Member['DocID']}'")
        #DB.PrintAllTables()


#SQL("HouseStockTrades.db").PrintAll('FinancialDisclosure')
# SQL("HouseStockTrades.db").ClearDB()
# SQL("HouseStockTrades.db").CreateTables()

#print(SQL("HouseStockTrades.db").Query("DELETE from FinancialDisclosure where year in ('2024', '2023', '2022', '2021')"))
# print(SQL("HouseStockTrades.db").Query('select distinct year from FinancialDisclosure'))
# FC = FinanceDisclosure()
from pdfquery import PDFQuery
from pdfminer.high_level import extract_text
# print(extract_text('__TMP__.pdf') )


class Transactions:
    def __init__(self) -> None:
        self.FirstYear = 2008
        self.CurrentYear = int(datetime.date.today().year)
        self.URLS = []
        self.DB = SQL("HouseStockTrades.db")

        self.GenerateURLS()


        self.Run()
        self.DB.Close()
    @staticmethod
    def Url(Year: int, doc) -> str:
        return f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{str(Year)}/{str(doc)}.pdf'
    def GenerateURLS(self):
        #print( self.CurrentYear)
        DoesExist = []
        for x in self.DB.Query('select distinct FilingId from Transactions'):
            DoesExist.append(x[0])


        AllDocs = []
        for x in self.DB.Query("select distinct DocID,Year from FinancialDisclosure where FilingType like 'p'"):
            AllDocs.append([x[0],x[1]])



        for Doc in AllDocs:
            #print(self.CurrentYear-2)
            if Doc[0] not in DoesExist:
                
                self.URLS.append(self.Url(Doc[1],Doc[0]))
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
    @staticmethod
    def CleanMember(StringDict):
        for x in StringDict:
            try:
                StringDict[x] = StringDict[x].replace('"','').replace("'",'')
            except:
                pass
    @staticmethod
    def Name(XMLSTR):
        return XMLSTR.split('Status:')[1].split('">')[2].split('</LTTextBoxHorizontal></LTTextLineHorizontal>')[0].replace('Hon.', '').replace('Mr.', '').replace('Ms.', '').replace('Mrs.', '').strip()
    @staticmethod
    def DistrictState(XMLSTR):
        return XMLSTR.split('State/District:')[1].split('</LTTextBoxHorizontal></LTTextLineHorizontal>')[0].strip()
    @staticmethod
    def TransactionNameList(XMLSTR):
        SPLIT = XMLSTR.split('">')
        for x in range(len(SPLIT)):
            SPLIT[x] = SPLIT[x].split('</LTTextBoxHorizontal></LTTextLineHorizontal>')[0].strip()
        OUTPUT = []
        for x in SPLIT:
            if '(' in x  and ')' in x:
                OUTPUT.append(x)
        return OUTPUT
    
    def TransactionsDict(self,XMLSTR):
        SPLIT = XMLSTR.split('">')
        for x in range(len(SPLIT)):
            SPLIT[x] = SPLIT[x].split('</LTTextBoxHorizontal></LTTextLineHorizontal>')[0].strip()
        OUTPUT = {}
        LIST = self.TransactionNameList(XMLSTR)
        
        for x in range(len(LIST)):
            #print(x)
            #print(len(LIST) -1)
            if x == len(LIST) -1 :
                BETWEEN = XMLSTR.split(LIST[x])[1]
            else:
                BETWEEN = XMLSTR.split(LIST[x])[1].split(LIST[x+1])[0]
            #print(LIST[x])
            OUTPUT[LIST[x]] = BETWEEN
        return OUTPUT
    @staticmethod
    def FilingId(XMLSTR):
        return XMLSTR.split('Filing ID #')[1].split('</LTTextBoxHorizontal></LTTextLineHorizontal>')[0].strip()
         
     
    def Run(self):
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]
        del self.URLS[0]

        # del self.URLS[0]


        for URL in self.URLS:
            FILENAME = '__TMP__.pdf'
            __REQ = self.Downloadfile(URL)
            
            FS = open(FILENAME, 'wb')
            FS.write(__REQ.content)
            FS.close()


            pdf = PDFQuery(FILENAME)
            pdf.load()
            pdf.tree.write('pdfXML.txt', pretty_print = True)

            XMLSTR = str(etree.tostring(pdf.tree, pretty_print=False)).replace('stream="&lt;PDFStream(21)','')
        
            print(self.Name(XMLSTR))
            print(self.DistrictState(XMLSTR))
            print(self.FilingId(XMLSTR))
            print(self.TransactionNameList(XMLSTR))
            t = self.TransactionsDict(XMLSTR)
            for x in t:
                t[x] = t[x].split('">')
                __O__ = []
                for y in range(len(t[x])):
                    
                    t[x][y] = t[x][y].split("</LTTextBoxHorizontal></LTTextLineHorizontal>")[0]
                    if "<LT" not in t[x][y]:
                        __O__.append(t[x][y])
                t[x] = __O__
                for u in range(len(t[x])):
                    t[x][u] = t[x][u].strip()
                while True:
                    try:
                        t[x].remove("")
                    except:
                        break
                print(x)
                print(t[x])
            break
            if '2023' in URL:
                print(URL)


T = Transactions()