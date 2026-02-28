import logging
from logging import Logger
import logging.config
from typing import Any

from file_system_assistant.app.configs.constants import Constants
from file_system_assistant.app.configs.logging.logging_filters import ConsoleOnlyFilter
from file_system_assistant.app.services.container import Container

class FSALogger:
    def __init__(self) -> None:
        logging_config: dict[str, Any] = {
            "version": 1,
            "disable_existing_loggers": False,

            "filters": {
                "console_only": {
                    "()": ConsoleOnlyFilter
                }
            },

            "formatters": {
                "detailed": {
                    "format": "%(asctime)s [%(levelname)s] "
                              "%(name)s - %(module)s:%(lineno)d - "
                              "%(funcName)s() - %(message)s"
                },
                "console_simple": {  # added
                    "format": "%(message)s"
                }
            },

            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/app.log",
                    "maxBytes": 5_000_000,
                    "backupCount": 3,
                    "formatter": "detailed",
                    "level": "DEBUG",
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "console_simple",  # changed
                    "level": "DEBUG",
                    "filters": ["console_only"],
                },
            },

            "loggers": {
                Constants.LOGGER_NAME: {
                    "handlers": ["file", "console"],
                    "level": "DEBUG",
                    "propagate": False,
                }
            },

            "root": {
                "handlers": ["file"],
                "level": "WARNING",
            },
        }

        logging.config.dictConfig(logging_config)

    @staticmethod
    def init():
        FSALogger()
        logger = logging.getLogger(Constants.LOGGER_NAME)
        Container.singleton(Logger, lambda: logger)