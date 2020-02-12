from bot import *

import time
import sys

if len(sys.argv) > 1 and sys.argv[1] in ("-V", "--verbose", "-D", "--debug"):
    debug = True
else :
    debug = False

b = Bot(debug)
 
def runBot():
    starttime = time.time()
    while True:
        try:
            b.getUpdates()
            b.sendServiceMessages()
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
        except requests.exceptions.ConnectionError as e:
            if debug is True:
                print("Connection error: ", e)
            print("Waiting for internet connection...")
            time.sleep(5.0)
        except KeyboardInterrupt:
            print("See y'all folks!")
            exit()
    
if __name__ == "__main__":
    b.hello()
    if debug == True:
        print("Debugging mode active! You will see plenty of stdout, and messages will be logged to the database.")
    runBot()