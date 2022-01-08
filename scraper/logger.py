import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_custom_logger(name):
    cwd = str(os.getcwd())
    formatter_file = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    )
    try:
        os.makedirs(os.path.join(cwd, "logs"))
    except FileExistsError:
        pass
    path = os.path.join(cwd, "logs", "trace.log")
    handler = TimedRotatingFileHandler(path, when="d", interval=1, backupCount=10)
    logger = logging.getLogger(name)
    handler.setFormatter(formatter_file)
    logger.addHandler(handler)
    return logger
