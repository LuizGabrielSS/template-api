import colorlog
import logging

def handler_log():

    log_format = "%(log_color)s %(asctime)s | %(levelname)s - %(message)s"

    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    color_formatter = colorlog.ColoredFormatter(log_format, log_colors=log_colors, datefmt='%Y-%m-%d %H:%M:%S')

    handler = logging.StreamHandler()

    handler.setFormatter(color_formatter)

    return handler


def log_formatter(name):

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler_log())

    return logger


logger = log_formatter(__name__)