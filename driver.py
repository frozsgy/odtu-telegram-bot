from bot import *

import time
import sys

verbose = False
logging = False

for i in sys.argv:
    if i in ('--verbose', '-V'):
        verbose = True
    if i in ('--log', '-L'):
        logging = True

b = Bot(verbose, logging)


def run_bot(verbose=False, logging=False):
    starttime = time.time()
    while True:
        try:
            b.get_updates()
            b.send_service_messages()
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
        except requests.exceptions.ConnectionError as e:
            if verbose is True:
                print("Connection error: ", e)
            print("Waiting for internet connection...")
            time.sleep(5.0)
        except KeyboardInterrupt:
            print("See y'all folks!")
            exit()


if __name__ == "__main__":
    b.hello()
    if verbose is True:
        print("Verbose mode is active! You will see plenty of stdout.")
    if logging is True:
        print("Logging is active! Messages will be logged to the database.")
    run_bot()
