import requests
import datetime
from utils import sql_postgre
from zipfile import ZipFile
from io import BytesIO
import pathlib

from dateutil.parser import parse
from time import sleep
class Transactions:

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

    def main(self):


        current = self.Downloadfile("https://unitedstates.github.io/congress-legislators/legislators-current.csv").text
        old = self.Downloadfile("https://unitedstates.github.io/congress-legislators/legislators-historical.csv").text
        listcong = (current + old).split('\n')
        listcongzzz = {}
        for x in range(len(listcong)):
            listcong[x] = listcong[x].split(',')
            try:
                listcong[x] = [listcong[x][0].lower(), listcong[x][9].lower(),listcong[x][10].lower(),listcong[x][12].lower(),listcong[x][13].lower().replace('https://', '').replace('.house.gov', '').replace('www.', '').replace('.senate.gov', '') ]
            except:
                pass
            # print(listcong[x])



        FILE = open('out.csv', 'rb').read().decode('ISO-8859-1').replace('\r', '').split('\n')
        FILE2 = open('out2.csv', 'w')
        del FILE[-1]
        del listcong[0]
        for x in range(len(FILE)):

            TTYYY = FILE[x].split(",")
            DIS = TTYYY[5].lower()
            LASTNAME = TTYYY[4].lower()
            # if LASTNAME != 'sessions':
            #     continue
            firstwo = TTYYY[5][:2].lower()
            lastwo = TTYYY[5][2:].lower()
            # print(FILE[x])

            found = None
            for y in listcong:
                if len(y) > 3:
                    if y[2] == '':
                        y[2] = -1
                    try:

                        if int(lastwo) == int(y[2]):

                            if (firstwo) == (y[1]):

                                if (LASTNAME == y[0] or LASTNAME == y[4]):
                                    # print(FILE[x] )
                                    # print(y)
                                    found = True
                                    FILE2.write(FILE[x] + ',' + y[3] + '\n')
                                    break
                    except:
                        pass
            if not found:
                FILE2.write(FILE[x] + ','+ '\n')

                        



Transactions().main()