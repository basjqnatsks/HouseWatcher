import nasdaqdatalink
from read import read
class Nasdaq:
    def __init__(self) -> None:
        self.key = self.get_api_key()



    @staticmethod
    def get_api_key() -> str:
        return read('nasdaq.api')


Nasdaq()