import requests
import datetime
from sql import SQL
import json
from zipfile import ZipFile
from io import BytesIO
import pdfplumber
from lxml import etree
from dateutil.parser import parse
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
        return XMLSTR.split('name:')[1].split('\n')[0].replace('hon.', '').replace('mr.', '').replace('ms.', '').replace('mrs.', '').strip()
    @staticmethod
    def DistrictState(XMLSTR):
        return XMLSTR.split('state/district:')[1].split('\n')[0].strip()
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
        return XMLSTR.split('filing id')[1].split('\n')[0].strip().replace('#','')
         
     
    def Run(self):
        # print(len(self.URLS))
        for x in range(48+46+107):
            del self.URLS[0]

        i=1
        for URL in self.URLS:
            print(i)
            i+=1
            FILENAME = '__TMP__.pdf'
            __REQ = self.Downloadfile(URL)
            
            FS = open(FILENAME, 'wb')
            FS.write(__REQ.content)
            FS.close()
            XMLSTR = ""
            with pdfplumber.open('__TMP__.pdf') as pdf:
                for x in range(len(pdf.pages)):
                    first_page = pdf.pages[x]
                    XMLSTR += first_page.extract_text().lower()

            open('out.txt', 'w').write(XMLSTR)
            t = XMLSTR.split("type date")
            del t[0]
            #print(t)

            for x in range(len(t)):
                t[x] = t[x].split("initial public offerings")[0].split('filing status: new')
                del t[x][-1]
            # print(t)
            # # 
            # # 
            Trans = []
            for x in t:
                for y in x:
                    # if len(y) < 7:
                    #     print(y.encode('UTF-8'))
                    #     print('HA')
                    if y=='\n':
                        continue
                    Trans.append(y)
            
            for x in range(len(Trans)):

                DICT = {
                    'AMOUNT_LOW': None,
                    'AMOUNT_HIGH': None,
                    'NOTIF_DATE' : None,
                    'TRANS_DATE' : None,
                    'ASSET' : None,
                    'SUBHOLDING' : None,
                }
                
                TransString = Trans[x]
                if len(TransString) < 20 and "interest (" in TransString:
                    continue
                print('!'+TransString+'!')
                DICT['AMOUNT_HIGH'] = int(''.join(i for i in TransString.split('$')[-1] if i.isdigit()))

                DICT['AMOUNT_LOW'] = int(''.join(i for i in TransString.split('$')[-2] if i.isdigit()))
                
                ENDSTRING = TransString.split('$')[:-2][0].split('\n')[-1]
                try:
                    DATES = ENDSTRING.split(' s ')[1].strip().split(' ')
                except:
                    try:
                        DATES = ENDSTRING.split(' p ')[1].strip().split(' ')
                    except:
                        DATES = ENDSTRING.split(' e ')[1].strip().split(' ')
                DICT['TRANS_DATE'] = DATES[0]
                DICT['NOTIF_DATE'] = DATES[1]

                ASSET_TEMP = ENDSTRING.split(' s ')[0].split(' p ')[0].split(' e ')[0]

                DICT['ASSET'] = ASSET_TEMP
                #print(re.search(r'\d{2}/\d{2}/\d{2}', ASSET_TEMP))
                print(DICT)
                Trans[x] = DICT
            # print(XMLSTR)
            # print(self.Name(XMLSTR))
            # print(self.DistrictState(XMLSTR))
            # print(self.FilingId(XMLSTR))
            #print(self.TransactionNameList(XMLSTR))
            # t = self.TransactionsDict(XMLSTR)
            #break

