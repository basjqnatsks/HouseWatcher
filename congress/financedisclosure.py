import requests
import datetime
from sql import sql_postgre 
import xmltodict
from zipfile import ZipFile
from io import BytesIO
# Import the email modules we'll need
from email.message import EmailMessage
import smtplib
from time import sleep



class FinanceDisclosure:
    def __init__(self) -> None:
        self.EmailList = [
            '5095288130@vtext.com',
            '5092822020@vtext.com',
            '5095670431@vtext.com',
            '5094400337@vtext.com',
            '5097135671@txt.att.net',
            '5095540049@tmomail.net',
            '2027654320@txt.att.net',
        ]
        # self.SendEmail('Tewst')
        self.FirstYear = 2008
        self.CurrentYear = int(datetime.date.today().year)
        self.URLS = []
        self.DB = sql_postgre.SQLP("house")

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

    def SendEmail(self, messagwe):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("tutt21730@gmail.com", "nywd azmo nivs oyno")

        
        MSGS = messagwe
        for x in self.EmailList:
            msg = EmailMessage()
            msg['Subject'] = ""
            msg['From'] = "tutt21730@gmail.com"
            msg['To'] = x
            msg.set_content(MSGS)
            s.send_message(msg)


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
    def TUrl(Year: int, doc) -> str:
        return f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{str(Year)}/{str(doc)}.pdf'

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
                    DOESEXIST = self.DB.DoesFinanceExist(Member['DocID'])
                    # print(len(DOESEXIST))
                    if len(DOESEXIST) == 0:
                        self.CleanMember(Member)
                        # print(Member)
                        if not Member['FilingDate']:
                            Member['FilingDate'] = '01-01-1970'
                        
                        if Member['FilingType'].lower() == 'p':
                            self.SendEmail(f"""{Member['Last']} {self.TUrl(Member['Year'],Member['DocID'])}""")
                            print(f"""{Member['First']} {Member['Last']} Trade At {self.TUrl(Member['Year'],Member['DocID'])}""")
                        sleep(10)
                        self.DB.Insert('FinancialDisclosure', f"'{Member['First']}','{Member['Last']}','{Member['StateDst']}','{Member['FilingType']}','{Member['Year']}','{Member['FilingDate']}','{Member['DocID']}'")
        # #DB.PrintAllTables()
                        
FinanceDisclosure()

