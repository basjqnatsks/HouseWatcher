import requests
import datetime
from sql_postgre import SQLP
import json
from zipfile import ZipFile
from io import BytesIO
import pdfplumber
from lxml import etree
from dateutil.parser import parse
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
                if "$" in PreTransactions[x]:
                    JustTransactions.append(PreTransactions[x])




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
            NoDollarsSplitonSpace = NoDollars.split(' ')



            #clean up dollars
            for io in range(len(JustDollars)):
                JustDollars[io] = JustDollars[io].replace(',','').replace('-','').strip()
            
            #clean up NoDollars
            for io in range(len(NoDollarsSplitonSpace)):
                NoDollarsSplitonSpace[io] = NoDollarsSplitonSpace[io].strip()
            

            #find first date in list
            for PotentialTradeDate in NoDollarsSplitonSpace:
                if self.is_date(PotentialTradeDate):
                    DICT['TRANS_DATE'] = PotentialTradeDate
                    break


            #find last date in list
            for num in range(len(NoDollarsSplitonSpace)-1, -1, -1):

                if self.is_date(NoDollarsSplitonSpace[num]):
                    DICT['NOTIF_DATE'] = NoDollarsSplitonSpace[num]
                    break

            DICT['AMOUNT_LOW'] = JustDollars[0]
            DICT['AMOUNT_HIGH'] = JustDollars[1]

            # print(DICT)
            try:
                NoDollarsSplitonSpace.remove(DICT['NOTIF_DATE'])
            except:
                pass
            try:
                NoDollarsSplitonSpace.remove(DICT['TRANS_DATE'])
            except:
                pass

            DICT['TRANTYPE'] = NoDollarsSplitonSpace[-1]
            NotCombinedAsset = NoDollarsSplitonSpace[:-1]
            AssetString = ''
            for pqpw in NotCombinedAsset:
                AssetString += pqpw + ' '

            DICT['ASSET'] = AssetString.replace("'",'').replace(",",'').strip()
            
            
            # print(DICT)
            output.append(DICT)
        return output



    @staticmethod
    def CheckXMLversion(content):
        if "type date gains >\n$200?" in content:
            return 2
        if "type date" in content:
            return 1
        if len(content) == 0:
            return 0

    def main(self):
        FILENAME = '__TMP__.pdf'

        for x in range(876+15):
            del self.URLS[0]

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

            Transactions = []
            PageTransactions=[]
            if VersionInt == 1:
                PageTransactions = self.OldParse(XMLSTR)
                FileIDfromUrl = URL.split('.pdf')[0].split('/')[-1]
            elif VersionInt == 2:
                FileIDfromUrl = URL.split('.pdf')[0].split('/')[-1]
                pass
            elif VersionInt == 0:
                FileIDfromUrl = URL.split('.pdf')[0].split('/')[-1]
                self.DB.Query(f"INSERT INTO transactions VALUES ('','PICTURE','','01-01-1970',{FileIDfromUrl},-1,-1,'01-01-1970')")
                continue
            else:
                pass

            for TransDict in PageTransactions:
                if TransDict['AMOUNT_LOW'] and TransDict['AMOUNT_HIGH'] and TransDict['NOTIF_DATE'] and TransDict['TRANS_DATE'] and TransDict['ASSET']  and TransDict['TRANTYPE']:
                    # print(TransDict)
                    #print(f"INSERT INTO transactions VALUES ('{TransDict['TRANTYPE']}','{TransDict['ASSET']}','','{TransDict['TRANS_DATE']}',{FileIDfromUrl},{TransDict['AMOUNT_LOW']},{TransDict['AMOUNT_HIGH']},'{TransDict['NOTIF_DATE']}')")
                    self.DB.Query(f"INSERT INTO transactions VALUES ('{TransDict['TRANTYPE']}','{TransDict['ASSET']}','','{TransDict['TRANS_DATE']}',{FileIDfromUrl},{TransDict['AMOUNT_LOW']},{TransDict['AMOUNT_HIGH']},'{TransDict['NOTIF_DATE']}')")
                    # print(TransDict)
            continue



            for x in range(len(t)):
                t[x] = t[x].split("initial public offerings")[0]
                t[x] =t[x].split('filing status: new')
                # print(len(t[x]))
                if len(t[x]) == 1:
                    t[x] = t[x][0]
                    t[x].split('filing status: amended')
                else:
                    del t[x][-1]
            
            Trans = []
            for x in t:
                # print(x)
                for y in x:
                    if y=='\n':
                        continue
                    Trans.append(y)
            print(t)
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
                # print('!'+TransString+'!')
                try:
                    tza = TransString.split('$')
                except:
                    continue
                CON = 1
                #print(tza)
                for z in tza:
                    # print(z)
                    try:
                        z.split(' s ')[1]
                        DATES = z.split(' s ')[-1].strip().split(' ')
                        CON = None
                        break
                    except:
                        try:
                            z.split(' p ')[1]
                            DATES = z.split(' p ')[-1].strip().split(' ')
                            CON = None
                            break
                        except:
                            try:
                                z.split(' e ')[1]
                                DATES = z.split(' e ')[-1].strip().split(' ')
                                CON = None
                                break
                            except:
                                pass
                            #print(TransString.split('$')[:-2][-1].split('\n'))
                            #del ENDSTRING[-1]
                #print(TransString)  
                #print(z.split(' s ')[-1])
                if CON:
                    #print('CON')
                    continue
                #print(DATES)
                TYU = TransString.split('$')
                if len(''.join(i for i in TYU[-1] if i.isdigit())) == 0:
                    del TYU[-1]
                #print(TYU)
                DICT['TRANS_DATE'] = DATES[0]
                DICT['NOTIF_DATE'] = DATES[1]
                DICT['AMOUNT_HIGH'] = int(''.join(i for i in TYU[-1] if i.isdigit()))
                DICT['AMOUNT_LOW'] = int(''.join(i for i in TYU[-2] if i.isdigit()))
                print(TYU)
                while len(TYU) > 1:
                    del TYU[-1]
                tza = TYU
                ENDSTRING = tza[-1].split('\n')[-1]
                
                ASSET_TEMP = ENDSTRING.split(' s ')[0].split(' p ')[0].split(' e ')[0]
                if ASSET_TEMP == '':
                    TYU = TransString.split('$')
                    del TYU[0]
                    while len(TYU) > 1:
                        del TYU[-1]
                    tza = TYU
                    ENDSTRING = tza[-1].split('\n')[-1]
                    ASSET_TEMP = ENDSTRING.split(' s ')[0].split(' p ')[0].split(' e ')[0]

                DICT['ASSET'] = ASSET_TEMP

                #print(re.search(r'\d{2}/\d{2}/\d{2}', ASSET_TEMP))
                print(DICT)
                Trans[x] = DICT

            if Trans == []:
                t = XMLSTR.split("type date gains >\n$200?")[1].split('f s: new')
                print(t)
                for x in t:
                    Trans.append(x)
                    


            # print(Trans)
            # print(XMLSTR)
            # print(self.Name(XMLSTR))
            # print(self.DistrictState(XMLSTR))
            DICT['FILID'] = self.FilingId(XMLSTR)
            #print(self.TransactionNameList(XMLSTR))
            # t = self.TransactionsDict(XMLSTR)
           #INSERT INTO transactions VALUES ('','','','','','jt apple inc. (aapl)','',)
            print(DICT)
            # print(self.is_date(str(DICT['NOTIF_DATE'])))
            if DICT['ASSET'] and DICT['ASSET'] != '' and DICT['FILID'] and DICT['AMOUNT_HIGH'] and DICT['AMOUNT_LOW'] and DICT['NOTIF_DATE']:
                DICT['ASSET']= DICT['ASSET'].replace("'",'')
                try:
                    int(DICT['AMOUNT_LOW'])
                    int(DICT['AMOUNT_HIGH'])
                    int(DICT['FILID'])
                    
                except:
                    # print('Skip')
                    continue
                if DICT['AMOUNT_HIGH'] < 150010600 and  DICT['AMOUNT_LOW'] < 150010600 and self.is_date(str(DICT['NOTIF_DATE'])):
                    # print(DICT['NOTIF_DATE'])
                    # print('Sent')
                    self.DB.Query(f"INSERT INTO transactions VALUES ('','{DICT['ASSET']}','','01-01-1970',{DICT['FILID']},'01-01-1970',{DICT['AMOUNT_LOW']},{DICT['AMOUNT_HIGH']},'{DICT['NOTIF_DATE']}')")

            break

Transactions()