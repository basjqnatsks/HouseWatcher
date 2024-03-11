import requests
import datetime
from sql_postgre import SQLP
import json
from zipfile import ZipFile
from io import BytesIO
import pdfplumber
from lxml import etree
from dateutil.parser import parse
from time import sleep
import copy
class Transactions:
    def __init__(self) -> None:
        self.FirstYear = 2008
        self.CurrentYear = int(datetime.date.today().year)
        self.URLS = []
        self.DB = SQLP("house")

        self.GenerateURLS()
        self.main()
        self.DB.Close()
    @staticmethod
    def Url(Year: int, doc) -> str:
        return f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{str(Year)}/{str(doc)}.pdf'
    def GenerateURLS(self):
        # print( self.CurrentYear)
        # DoesExist = []
        # for x in self.DB.Query('select distinct FilingId from Transactions'):
        #     DoesExist.append(x[0])
        AllDocs = []
        for x in self.DB.Query("select distinct DocID,Year from FinancialDisclosure where FilingType like 'P'"):
            AllDocs.append([x[0],x[1]])
        for Doc in AllDocs:
            #print(self.CurrentYear-2)
            # if Doc[0] ==20006946:
            #     print(self.DB.DoesTransDocExist(x[0]))
            DOESEXIST = self.DB.DoesTransDocExist(Doc[0])
            if len(DOESEXIST) == 0:
                self.URLS.append(self.Url(Doc[1],Doc[0]))
        # print(self.URLS)
    @staticmethod
    def Downloadfile(URL):
        #try to send reqeuest forever sleep every 10 seconds
        while True:
            try:
                RTRE = requests.get(URL)
            #print Exception
            except Exception as f:
                print(f)
                sleep(10)
            else:
                break
        return RTRE
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
    def is_date(string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try: 
            if "/" not in string:
                return False
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False
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
    @staticmethod
    def __dumppdf(content):
        FILENAME = '__TMP__.pdf'
        FS = open(FILENAME, 'wb')
        FS.write(content)
        FS.close()
    @staticmethod
    def PdftoText():
        XMLSTR = "" 
        with pdfplumber.open('__TMP__.pdf') as pdf:
            for x in range(len(pdf.pages)):
                first_page = pdf.pages[x]
                XMLSTR += first_page.extract_text().lower()
        XMLSTR = XMLSTR.encode('ISO 8859-1', 'ignore').decode('ISO 8859-1','ignore')
        return XMLSTR
    def OldParse(self, content):
        output = []
        TransSplit = content.split("type date\n")
        #delete before transactions
        del TransSplit[0]
        TransSplit[-1]  = TransSplit[-1].split("asset class details")[0]
        PreTransactions = []
        for TMP in TransSplit:
            for x in TMP.split('\n'):
                PreTransactions.append(x )
        #remove empties
        while True:
            try:
                PreTransactions.remove('')
            except:
                break
        JustTransactions = []
        for x in range(len(PreTransactions)):
            if "filing status:" not in PreTransactions[x] and "subholding of:" not in PreTransactions[x] and "description:" not in PreTransactions[x]:
                # print(PreTransactions[x])
                if "$" in PreTransactions[x]:
                    JustTransactions.append(PreTransactions[x])
        # print(JustTransactions)
        for x in JustTransactions:
            # print(x)
            DICT = {
            'AMOUNT_LOW': None,
            'AMOUNT_HIGH': None,
            'NOTIF_DATE' : None,
            'TRANS_DATE' : None,
            'ASSET' : None,
            'SUBHOLDING' : None,
            'TRANTYPE': None
            }
            SplitOnDollar = x.split('$')
            JustDollars = SplitOnDollar[-2:]
            NoDollars = SplitOnDollar[0].strip()
            print(NoDollars)
            NoDollarsSplitonSpace = NoDollars.split(' ')
            # print(SplitOnDollar)
            #clean up dollars
            for io in range(len(JustDollars)):
                JustDollars[io] = JustDollars[io].replace(',','').replace('-','').strip()
            #clean up NoDollars
            for io in range(len(NoDollarsSplitonSpace)):
                NoDollarsSplitonSpace[io] = NoDollarsSplitonSpace[io].strip()
            #find second last date
           #find last date in list
            psoie = 0 
            for num in range(len(NoDollarsSplitonSpace)-1, -1, -1):
                if self.is_date(NoDollarsSplitonSpace[num]):
                    if psoie == 1:
                        DICT['TRANS_DATE'] = NoDollarsSplitonSpace[num]
                        break
                    psoie += 1 
            #find last date in list
            for num in range(len(NoDollarsSplitonSpace)-1, -1, -1):

                if self.is_date(NoDollarsSplitonSpace[num]):
                    DICT['NOTIF_DATE'] = NoDollarsSplitonSpace[num]
                    break
            # print(JustDollars)
            try:
                int(JustDollars[0])
                DICT['AMOUNT_LOW'] = JustDollars[0]
            except:
                DICT['AMOUNT_LOW'] = -1
            try :
                int(JustDollars[1])
                DICT['AMOUNT_HIGH'] = JustDollars[1]
            except:
                DICT['AMOUNT_HIGH'] = -1
            # print(DICT)
            try:
                NoDollarsSplitonSpace.remove(DICT['NOTIF_DATE'])
            except:
                pass
            try:
                NoDollarsSplitonSpace.remove(DICT['TRANS_DATE'])
            except:
                pass
            #find last date in list
            for num in range(len(NoDollarsSplitonSpace)-1, -1, -1):
                if not self.is_date(NoDollarsSplitonSpace[num]) and len(NoDollarsSplitonSpace[num]) == 1:
                    DICT['TRANTYPE'] = NoDollarsSplitonSpace[num]
                    break
            NotCombinedAsset = NoDollarsSplitonSpace[:-1]
            AssetString = ''
            for pqpw in NotCombinedAsset:
                AssetString += pqpw + ' '
            DICT['ASSET'] = AssetString.replace("'",'').replace(",",'').strip()
            print(DICT)
            output.append(DICT)
        # print(output)
        return output
    def NewParse(self, content):
        output = []
        #remove button out
        content = content.replace('id owner asset transaction date notification amount cap.','').replace('(partial)','')
        TransSplit = content.split("type date gains >\n$200?")
        #delete before transactions
        del TransSplit[0]

        #remove last element delimiter EOD
        TransSplit[-1]  = TransSplit[-1].split("asset class details")[0]
        PreTransactions = []
        for TMP in TransSplit:
            for x in TMP.split('\n'):
                PreTransactions.append(x )
        #remove empties
        while True:
            try:
                PreTransactions.remove('')
            except:
                break
        JustTransactions = []
        for x in range(len(PreTransactions)):
            if "filing status:" not in PreTransactions[x] and "subholding of:" not in PreTransactions[x] and "description:" not in PreTransactions[x]:
                # print(PreTransactions[x])
                if "$" in PreTransactions[x] and len(PreTransactions[x]) > 20 and 'gfe' in PreTransactions[x]:
                    JustTransactions.append(PreTransactions[x].replace('gfedcb', 'gfedc').replace('gfedc\n', ''))

        for x in JustTransactions:
            
            DICT = {
            'AMOUNT_LOW': None,
            'AMOUNT_HIGH': None,
            'NOTIF_DATE' : None,
            'TRANS_DATE' : None,
            'ASSET' : None,
            'SUBHOLDING' : None,
            'TRANTYPE': None
            }
            SplitOnSpace = x.split(' ')
            #JustDollars = SplitOnDollar[-2:]
            #print(SplitOnSpace)

            MoneyCounter = 0
            for num in range(len(SplitOnSpace)-1, -1, -1):
                if '$' in SplitOnSpace[num]:
                    if MoneyCounter == 0 and not DICT['AMOUNT_LOW']:
                        DICT['AMOUNT_LOW'] = SplitOnSpace[num].replace('$','').replace(',','')
                    if MoneyCounter == 1 and not DICT['AMOUNT_HIGH']:
                        DICT['AMOUNT_HIGH'] = SplitOnSpace[num].replace('$','').replace(',','')
                    MoneyCounter += 1 
            if not DICT['AMOUNT_HIGH']:
                DICT['AMOUNT_HIGH'] = '-1'


            NoDollars = x.split(DICT['AMOUNT_HIGH'])[0]
            NoDollarsSplitOnSpace = NoDollars.split(' ')

            DateCounter = 0
            for num in range(len(NoDollarsSplitOnSpace)-1, -1, -1):
                if self.is_date(NoDollarsSplitOnSpace[num]):
                    if DateCounter == 0 and not DICT['NOTIF_DATE']:
                        DICT['NOTIF_DATE'] = NoDollarsSplitOnSpace[num]
                    if DateCounter == 1 and not DICT['TRANS_DATE']:
                        DICT['TRANS_DATE'] = NoDollarsSplitOnSpace[num]
                    DateCounter += 1 

            while True:
                try:
                    NoDollarsSplitOnSpace.remove('$')
                except:
                    break
            
            for num in range(len(NoDollarsSplitOnSpace)-1, -1, -1):
                if not self.is_date(NoDollarsSplitOnSpace[num]) and len(NoDollarsSplitOnSpace[num]) == 1 and NoDollarsSplitOnSpace[num] in ['p', 's', 'a','e']:
                    DICT['TRANTYPE'] = NoDollarsSplitOnSpace[num]
                    break


            #combine String 
            AssetString = ''
            for pqpw in NoDollarsSplitOnSpace:
                AssetString += pqpw + ' '
            print(AssetString)
            DICT['ASSET'] = AssetString.replace("'",'').replace(",",'').strip().split(' '+DICT['TRANTYPE']+' ')[0].strip()
            print(DICT)
            output.append(DICT)
        return output
    def NewNullParse(self, content):
        output = []
        #remove button out
        content = content.replace('id owner asset transaction date notification amount cap.','').replace('(partial)','').replace('\x00','')
        TransSplit = content.split("type date gains >\n$200?")
        #delete before transactions
        del TransSplit[0]

        #remove last element delimiter EOD
        TransSplit[-1]  = TransSplit[-1].split("* for the complete list of asset type abbreviations")[0]
        PreTransactions = []
        for TMP in TransSplit:
            for x in TMP.split('\n'):
                PreTransactions.append(x )
        # print(PreTransactions)
        #remove empties
        while True:
            try:
                PreTransactions.remove('')
            except:
                break
        JustTransactions = []
        for x in range(len(PreTransactions)):
            if "filing status:" not in PreTransactions[x] and "subholding of:" not in PreTransactions[x] and "description:" not in PreTransactions[x]:
                # print(PreTransactions[x])
                if "$" in PreTransactions[x] and len(PreTransactions[x]) > 20 :
                    JustTransactions.append(PreTransactions[x].replace('gfedcb', 'gfedc').replace('gfedc\n', ''))
        print(JustTransactions)
        for x in JustTransactions:
            
            DICT = {
            'AMOUNT_LOW': None,
            'AMOUNT_HIGH': None,
            'NOTIF_DATE' : None,
            'TRANS_DATE' : None,
            'ASSET' : None,
            'SUBHOLDING' : None,
            'TRANTYPE': None
            }
            SplitOnSpace = x.split(' ')
            #JustDollars = SplitOnDollar[-2:]
            #print(SplitOnSpace)

            MoneyCounter = 0
            for num in range(len(SplitOnSpace)-1, -1, -1):
                if '$' in SplitOnSpace[num]:
                    if MoneyCounter == 0 and not DICT['AMOUNT_LOW']:
                        DICT['AMOUNT_LOW'] = SplitOnSpace[num].replace('$','').replace(',','')
                    if MoneyCounter == 1 and not DICT['AMOUNT_HIGH']:
                        DICT['AMOUNT_HIGH'] = SplitOnSpace[num].replace('$','').replace(',','')
                    MoneyCounter += 1 
            if not DICT['AMOUNT_HIGH']:
                DICT['AMOUNT_HIGH'] = '-1'


            NoDollars = x.split(DICT['AMOUNT_HIGH'])[0]
            NoDollarsSplitOnSpace = NoDollars.split(' ')

            DateCounter = 0
            for num in range(len(NoDollarsSplitOnSpace)-1, -1, -1):
                if self.is_date(NoDollarsSplitOnSpace[num]):
                    if DateCounter == 0 and not DICT['NOTIF_DATE']:
                        DICT['NOTIF_DATE'] = NoDollarsSplitOnSpace[num]
                    if DateCounter == 1 and not DICT['TRANS_DATE']:
                        DICT['TRANS_DATE'] = NoDollarsSplitOnSpace[num]
                    DateCounter += 1 

            while True:
                try:
                    NoDollarsSplitOnSpace.remove('$')
                except:
                    break
            
            for num in range(len(NoDollarsSplitOnSpace)-1, -1, -1):
                if not self.is_date(NoDollarsSplitOnSpace[num]) and len(NoDollarsSplitOnSpace[num]) == 1 and NoDollarsSplitOnSpace[num] in ['p', 's', 'a','e']:
                    DICT['TRANTYPE'] = NoDollarsSplitOnSpace[num]
                    break


            #combine String 
            AssetString = ''
            for pqpw in NoDollarsSplitOnSpace:
                AssetString += pqpw + ' '
            print(NoDollarsSplitOnSpace)
            try:
                DICT['ASSET'] = AssetString.replace("'",'').replace(",",'').strip().split(' '+DICT['TRANTYPE']+' ')[0].strip()
            except TypeError:
                DICT['ASSET'] = None
            print(DICT)
            output.append(DICT)
        return output
    @staticmethod
    def CheckXMLversion(content):
        if "type date gains >\n$200?" in content and not 'gfe'in content:
            return 3
        if "type date gains >\n$200?" in content:
            return 2
        if "type date" in content:
            return 1
        if len(content) == 0:
            return 0
    def main(self):
        FILENAME = '__TMP__.pdf'
        print(len(self.URLS))
        return
        # for x in range(1695+16+37):
        #     del self.URLS[0]

        UrlIter=1
        #Iterate through all premade urls
        for URL in self.URLS:
            #Number Counter
            print(UrlIter)
            UrlIter+=1



            __Request__ = self.Downloadfile(URL)
            self.__dumppdf(__Request__.content)

            XMLSTR = self.PdftoText()
            open('out.txt', 'w').write(XMLSTR)


            VersionInt = self.CheckXMLversion(XMLSTR)
            # print(VersionInt)
            Transactions = []
            PageTransactions=[]
            if VersionInt == 1:
                PageTransactions = self.OldParse(XMLSTR)
                FileIDfromUrl = URL.split('.pdf')[0].split('/')[-1]
            elif VersionInt == 2:
                PageTransactions = self.NewParse(XMLSTR)
                FileIDfromUrl = URL.split('.pdf')[0].split('/')[-1]
            elif VersionInt == 3:
                PageTransactions = self.NewNullParse(XMLSTR)
                FileIDfromUrl = URL.split('.pdf')[0].split('/')[-1]
            elif VersionInt == 0:
                FileIDfromUrl = URL.split('.pdf')[0].split('/')[-1]
                self.DB.Query(f"INSERT INTO transactions VALUES ('','PICTURE','','01-01-1970',{FileIDfromUrl},-1,-1,'01-01-1970')")
                continue
            else:
                pass
            
            for TransDict in PageTransactions:
                if TransDict['AMOUNT_LOW'] and TransDict['AMOUNT_HIGH'] and TransDict['NOTIF_DATE'] and TransDict['TRANS_DATE'] and TransDict['ASSET']  and TransDict['TRANTYPE']:
                    #print(f"INSERT INTO transactions VALUES ('{TransDict['TRANTYPE']}','{TransDict['ASSET']}','','{TransDict['TRANS_DATE']}',{FileIDfromUrl},{TransDict['AMOUNT_LOW']},{TransDict['AMOUNT_HIGH']},'{TransDict['NOTIF_DATE']}')")
                    self.DB.Query(f"INSERT INTO transactions VALUES ('{TransDict['TRANTYPE']}','{TransDict['ASSET']}','','{TransDict['TRANS_DATE']}',{FileIDfromUrl},{TransDict['AMOUNT_LOW']},{TransDict['AMOUNT_HIGH']},'{TransDict['NOTIF_DATE']}')")
                    # print(TransDict)
            continue
            



Transactions()