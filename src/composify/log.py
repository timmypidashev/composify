# system
import os
import sys
import asyncio
import traceback
from dotenv import load_dotenv
import logging
import logging.config
import coloredlogs
from logging.handlers import TimedRotatingFileHandler

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
# define a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(message)s'))

# degfine a file handler
file_handler = TimedRotatingFileHandler(
    filename=log_file,
    when="D",
    backupCount=0,
    encoding="utf-8",
    delay=False,
    utc=False
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
)

# add handlers
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(file_handler)
    
# create composify logger
composify_logger = logging.getLogger("composify")
composify_logger.setLevel(logging.DEBUG)
composify_logger.addHandler(console_handler)
composify_logger.addHandler(file_handler)
composify_logger.propagate = False

# create db logger
db_logger = logging.getLogger("db")
db_logger.setLevel(logging.DEBUG)
db_logger.addHandler(file_handler)
db_logger.propagate = False


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
        #coloredlogs.install(level="INFO", logger=self.logger)

        # install colored log output for external 'root' instances such as pycord
        #coloredlogs.install(level=None)
        
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

