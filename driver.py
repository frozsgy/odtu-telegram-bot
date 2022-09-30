import sys
import time

from bot import *

is_verbose = False
logging_enabled = False

for i in sys.argv:
    if i in ('--verbose', '-V'):
        is_verbose = True
    if i in ('--log', '-L'):
        logging_enabled = True

b = Bot(logging_enabled)


def run_bot(verbose=False):
    start_time = time.time()
    while True:
        try:
            b.get_updates()
            b.send_service_messages()
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))
        except requests.exceptions.ConnectionError as e:
            if verbose is True:
                logging.critical("Connection error: ", e)
            logging.info("Waiting for internet connection...")
            time.sleep(5.0)
        except KeyboardInterrupt:
            logging.info("See y'all folks!")
            exit()


if __name__ == "__main__":
    b.hello()
    if is_verbose is True:
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Verbose mode is active! You will see plenty of debug information.")
    else:
        logging.basicConfig(level=logging.INFO)
    if logging_enabled is True:
        logging.info("Logging is active! Messages will be logged to the database.")
    run_bot()
