from financedisclosure import FinanceDisclosure
# from transactions import Transactions
# from sql import SQL

# SQL("HouseStockTrades.db").PrintAll('FinancialDisclosure')
# SQL("HouseStockTrades.db").ClearDB()
# SQL("HouseStockTrades.db").CreateTables()

#print(SQL("HouseStockTrades.db").Query("DELETE from FinancialDisclosure where year in ('2024', '2023', '2022', '2021')"))
# print(SQL("HouseStockTrades.db").Query('select distinct year from FinancialDisclosure'))
FC = FinanceDisclosure()
# from pdfquery import PDFQuery
# from pdfminer.high_level import extract_text
# print(extract_text('__TMP__.pdf') )

# import psycopg2

# connection = psycopg2.connect(database="house", user="postgres", password="pass", host="localhost", port=5432)

# cursor = connection.cursor()

# # cursor.execute("select * from information_schema.tables where table_schema = 'public';")

# cursor.execute("INSERT INTO movie VALUES ('test','test',1)")

# connection.commit()
# Fetch all rows from database
# record = cursor.fetchall()

# print("Data from Database:- ", record)

# T = Transactions()