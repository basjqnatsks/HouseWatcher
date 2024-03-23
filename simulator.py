from sql_postgre import SQLP


class simulate:


    def __new__(cls,Security,BuyDate,SellDate,Amount):
        return cls.__init__(cls,Security,BuyDate,SellDate,Amount)
    
    def __init__(self,Security,BuyDate,SellDate,Amount) -> None:
        self.DB = SQLP("house")

        BuyQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice >= '{BuyDate}' order by dateprice ASC limit 1"
        SellQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice <= '{SellDate}' order by dateprice desc limit 1"
        print(SellQ)
        BuyPrice = float(self.DB.Query(BuyQ)[0][0].replace('$', ''))
        SellPrice = float(self.DB.Query(SellQ)[0][0].replace('$', ''))
        self.DB.Close()
        return (SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2))
    

  

print(simulate('rick', '2019-01-01', '2024-03-23', 5000))