import nasdaqdatalink
from read import read
class Nasdaq:
    def __init__(self) -> None:
        self.key = self.get_api_key()
        nasdaqdatalink.read_key(filename="nasdaq.api")
        data = nasdaqdatalink.get('NSE/OIL')
        #data = nasdaqdatalink.get_table('ZACKS/FC', ticker='AAPL')
    
        print(data)
    @staticmethod
    def get_api_key() -> str:
        return read('nasdaq.api')


Nasdaq()