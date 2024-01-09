# system
import os
import sys
import asyncio
import traceback
from dotenv import load_dotenv
import logging
import logging.config
from colorama import init, Fore, Style
from logging.handlers import TimedRotatingFileHandler

# Initialize colorama to work with ANSI escape codes
init(autoreset=True)

# Make sure we have a proper log output path
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
class ConsoleFormatter(logging.Formatter):
    """
    The console log outputs will be colorized with this formatter,
    along simplifications so that only the data a user needs will be shown.
    """
    COLORS = {
        "DEBUG": Style.DIM + Fore.BLUE,
        "INFO": Style.NORMAL + Fore.GREEN,
        "WARNING": Style.BRIGHT + Fore.YELLOW,
        "ERROR": Style.BRIGHT + Fore.RED,
        "CRITICAL": Style.BRIGHT + Fore.MAGENTA,
    }

    def format(self, record):
        log_message = super().format(record)
        log_level = record.levelname

        color = self.COLORS.get(log_level, '')
        return f"{color}{log_message}"

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(ConsoleFormatter())

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

    @staticmethod
    def check_debug_logging(debug):
        """
        * Set the logging level from 'INFO' to 'DEBUG' if True
        * Logs 'db' not only to file, but console as well.

        Args:
            debug (bool): set logging to debug or not? (e.g., True or False)
        """
        if debug:
            # Set the level for the console handler
            console_handler.setLevel(logging.DEBUG)

        else:
            return
