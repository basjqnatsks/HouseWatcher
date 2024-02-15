from financedisclosure import FinanceDisclosure
from transactions import Transactions


#SQL("HouseStockTrades.db").PrintAll('FinancialDisclosure')
# SQL("HouseStockTrades.db").ClearDB()
# SQL("HouseStockTrades.db").CreateTables()

#print(SQL("HouseStockTrades.db").Query("DELETE from FinancialDisclosure where year in ('2024', '2023', '2022', '2021')"))
# print(SQL("HouseStockTrades.db").Query('select distinct year from FinancialDisclosure'))
# FC = FinanceDisclosure()
# from pdfquery import PDFQuery
# from pdfminer.high_level import extract_text
# print(extract_text('__TMP__.pdf') )




T = Transactions()