import logging
import sys
import time

from bot import *
from logger import logger


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
            logger.info("Waiting for internet connection...")
            time.sleep(5.0)
        except KeyboardInterrupt:
            logger.info("See y'all folks!")
            exit()


if __name__ == "__main__":
    logging_enabled = False
    is_verbose = False

    for i in sys.argv:
        if i in ('--verbose', '-V'):
            is_verbose = True
            logger.root.setLevel(logging.DEBUG)
            logger.getLogger("urllib3").setLevel(logging.WARNING)
        if i in ('--log', '-L'):
            logging_enabled = True

    b = Bot(logging_enabled)

    if is_verbose:
        logger.info("Verbose mode is active! You will see plenty of debug information.")
    if logging_enabled:
        logger.info("Logging is active! Messages will be logged to the database.")

    b.hello()
    run_bot()
