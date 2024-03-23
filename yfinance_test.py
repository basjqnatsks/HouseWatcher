import yfinance as yf
import requests
import requests
import threading
from queue import Queue
TEST = []


class Threadit:
    ThreadedArray = []

	
    #function Requires 
    def __init__(self, FunctionPointer, WorkLoadArray, ThreadCount = 1) -> None:
        self.ThreadCount = ThreadCount
        print(ThreadCount)
        self.WorkLoadArray = WorkLoadArray
        def threader():
            while True:
                a = queue.get()
                if a == None:
                    break
                FunctionPointer(a[0], a[1])
                queue.task_done()
                
        queue = Queue()
        for x in range(self.ThreadCount):
            t = threading.Thread(target=threader)
            t.daemon = True
            self.ThreadedArray.append(t)
            t.start()
            
        for x in range(len(self.WorkLoadArray)):
            queue.put([self.WorkLoadArray[x], x])

        for i in range(self.ThreadCount):
            queue.put(None)
        for t in self.ThreadedArray:
            t.join()



def __ThreadedFunction(WorkLoad, ThreadId):
    try:
        yf.download(WorkLoad[0], '1900-01-01', '2025-01-01').to_csv(f'test/{WorkLoad[0]}.csv')
    except:
        pass



import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',

    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

response = requests.get('https://www.sec.gov/include/ticker.txt', headers=headers)
TICKER_LIST = str(response.text)
TICKER_LIST = TICKER_LIST.split('\n')
for x in range(len(TICKER_LIST)):
    TICKER_LIST[x] = TICKER_LIST[x].split('\t')
print(TICKER_LIST)

Threadit(__ThreadedFunction, TICKER_LIST, ThreadCount=1)
print(len(TEST))