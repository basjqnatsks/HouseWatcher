import requests
import datetime
from sql import SQL
import xmltodict
from zipfile import ZipFile
from io import BytesIO
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
