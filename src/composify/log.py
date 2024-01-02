# system
import os
import sys
import asyncio
import traceback
from dotenv import load_dotenv
import logging
import logging.config
import coloredlogs

user_home = os.path.expanduser("~")
config_path = os.path.join(user_home, ".config", "composify")
log_file = f"{config_path}/composify.log"

try:
    if not os.path.exists(config_path):
        os.makedirs(config_path)

except Exception:
    # TODO: convert to error raised from composify.errors
    print("Only posix based systems are supported at the moment!")

# configure logging
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S]"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "when": "D",
            "backupCount": 0,
            "filename": log_file
        }
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"]
        },
        "composify": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
            "qualname": "client"
        },
        "db": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
            "qualname": "db"
        }
    }
}

logging.config.dictConfig(log_config)


class Logger:
    """
    Logger class.
    """

    def __init__(self, name):
        """
        Initialize a logger instance.
        """
        self.logger = logging.getLogger(name)

        # install colored log output for our logger instances
        coloredlogs.install(level="INFO", logger=self.logger)

        # install colored log output for external 'root' instances such as pycord
        coloredlogs.install(level=None)
        
    async def debug(self, message):
        """
        Log a debug message.
        """
        self.logger.debug(message)

    async def info(self, message):
        """
        Log an info message.
        """
        self.logger.info(message)

    async def warning(self, message):
        """
        Log a warning message.
        """
        self.logger.warning(message)

    async def error(self, message):
        """
        Log an error message.
        """
        self.logger.error(message)

    async def critical(self, message):
        """
        Log a critical message.
        """
        self.logger.critical(message)

