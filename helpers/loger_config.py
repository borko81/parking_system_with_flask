import logging
from abc import ABC, abstractmethod


class Logger(ABC):
    @staticmethod
    @abstractmethod
    def logme(message):
        pass


class LoggerInfo(Logger):
    def logme(message):
        log = logging.getLogger("werkzeug")
        log.disabled = True
        logging.basicConfig(
            filename="log_info.log",
            level=logging.INFO,
            format="%(asctime)s;%(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        logging.info(message)


class LoggerError(Logger):
    def logme(message):
        log = logging.getLogger("werkzeug")
        log.disabled = True
        logging.basicConfig(
            filename="log_error.log",
            level=logging.ERROR,
            format="%(asctime)s;%(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        logging.error(message)


logger_mapper = {"info": lambda: LoggerInfo, "error": lambda: LoggerError}


def custom_logger(name, message):
    return logger_mapper[name]().logme(message)
