from bot import *

import time

b = Bot()
 
def runBot():
    starttime = time.time()
    while True:
        try:
            b.getUpdates()
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
        except requests.exceptions.ConnectionError as errc:
            print("Connection error: ",errc)
            print("Waiting for internet connection...")
            time.sleep(5.0)
        except KeyboardInterrupt:
            print("See y'all folks!")
            exit()
            
            
    
    
if __name__ == "__main__":
    b.hello()
    runBot()