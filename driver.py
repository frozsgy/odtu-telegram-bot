from bot import *

import time

b = Bot()
 
def runBot():
    try:
        starttime = time.time()
        while True:
            b.getUpdates()
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
        
    except KeyboardInterrupt:
        print("See y'all folks!")
 

if __name__ == "__main__":
    b.hello()
    runBot()