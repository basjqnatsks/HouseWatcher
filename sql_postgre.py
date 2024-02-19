import psycopg2
class SQLP:
    def __init__(self, dbname ) -> None:
        self.connection = psycopg2.connect(database=dbname, user="postgres", password="pass", host="localhost", port=5432)


    # def Refresh(self):
    #     self.connection.close()
    #     self.connection = sqlite3.connect(self.dbname)
        

    def ClearDB(self):
        for x in self.GetAllTables():
            tablename = x[0]
            self.connection.cursor().execute("drop table "+ str(tablename))
            self.Refresh()
    # def CreateTables(self):
    #     self.connection.cursor().execute("CREATE TABLE movie(title, year, score)")
    #     self.connection.cursor().execute("CREATE TABLE FinancialDisclosure(FirstName, LastName, StateDistrict, FilingType, Year, FilingDate, DocID)")
    #     self.connection.cursor().execute("CREATE TABLE Transactions(FirstName, LastName, StateDistrict, TranType, Owner, Asset, Ticker, TransDate, FilingId,FilingDate,TradeDate,Amount,AmountLow,AmountHigh,NotificationDate)")
    #     self.Refresh()
    def PrintAllTables(self):
        print(self.GetAllTables())
    def GetAllTables(self):
        cur = self.connection.cursor()
        res = cur.execute("select * from information_schema.tables where table_schema = 'public';")
        OUT =[]
        for x in cur.fetchall():
            OUT.append(x[2])
        return OUT
    
    def Doesexist(self,DociD):
        cur = self.connection.cursor()
        QUERY = f"select 1 from FinancialDisclosure where docid = '{DociD}' limit 1"
        # print(QUERY)
        res = cur.execute(QUERY)
        OUT =cur.fetchall()
        # for x in cur.fetchall():
        #     OUT.append(x[2])
        return OUT


    def Insert(self, table, values):
        __C = self.connection.cursor()
        # print(f"INSERT INTO {table} VALUES ({values})")
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
    

# cursor = connection.cursor()

# cursor.execute("SELECT * from public.financialdisclosure;")

# # Fetch all rows from database
# record = cursor.fetchall()

# print("Data from Database:- ", record)
    
# s = SQL('house')
# s.PrintAllTables()