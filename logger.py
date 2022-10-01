import logging

logger = logging
logger.addLevelName(logging.CRITICAL, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))
logger.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logger.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logger.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logger.addLevelName(logging.DEBUG, "\033[1;35m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))

logger.basicConfig(format='[%(levelname)s:%(asctime)s] %(message)s', level=logging.INFO)
