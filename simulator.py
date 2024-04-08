from sql_postgre import SQLP


class simulate:



    def __init__(self,Security,BuyDate,SellDate,Amount) -> None:
        self.DB = SQLP("house")
        

        self.DB.Close()
        
    
    def test():
        BuyQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice >= '{BuyDate}' order by dateprice ASC limit 1"
        SellQ = f"select closeprice from simulator where ticker = '{Security}' and dateprice <= '{SellDate}' order by dateprice desc limit 1"
        print(SellQ)
        BuyPrice = float(self.DB.Query(BuyQ)[0][0].replace('$', ''))
        SellPrice = float(self.DB.Query(SellQ)[0][0].replace('$', ''))
        return (SellPrice-BuyPrice, round(SellPrice/BuyPrice,2), round(SellPrice/BuyPrice*Amount,2))

simulate()