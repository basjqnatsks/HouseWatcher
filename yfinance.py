from sql_postgre import SQLP
from read import read
import os
class yfinance:

    def __init__(self) -> None:
        self.Directory = 'test\\'
        self.DB = SQLP("house")
        print(len(self.readDirectory()))
        self.DB.Close()

    def UploadFromDisk(self):
        for x in os.listdir(self.Directory):
            var  = read(self.Directory+ x, '\n')
            del var[0]
            for y in range(len(var)):
                var[y] = var[y].split(',')
            

   

yfinance()