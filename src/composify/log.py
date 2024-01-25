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

class Logger:
    """
    Logger class.
    """

    # NOTE: console_handler and file_handler is defined here so 
    # that it can later be manipulated between classmethods!
    # NOTE: file_handler is 'None' here so that the log_file
    # can be properly added below once the Logger class knows
    # where to output logs!
    console_handler = logging.StreamHandler()
    file_handler = None 

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

    @classmethod
    def configure_log_path(cls, dev):
        """
        Make sure we have a proper log output path,
        taking into account dev builds are run in a 
        virtual environment, whereas prod builds are
        run on a unix-like system.
        """
        if dev:
            config_path = os.path.join(".dev")
            log_file = f"{config_path}/composify.dev.log"

        else:
            user_home = os.path.expanduser("~")
            config_path = os.path.join(user_home, ".config", "composify")
            log_file = f"{config_path}/composify.log"

        try:
            if not os.path.exists(config_path):
                os.makedirs(config_path)

        except Exception:
            # TODO: convert to error raised from composify.errors
            print("Only posix based systems are supported at the moment!")

        finally:
            return log_file
    
    @classmethod
    def configure_handlers(cls, log_file):
        """
        Create all handlers for the logger.
        """

        # configure handlers
        cls.file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="D",
            backupCount=0,
            encoding="utf-8",
            delay=False,
            utc=False
        )
        cls.console_handler.setLevel(logging.INFO)
        cls.console_handler.setFormatter(ConsoleFormatter())
        cls.file_handler.setLevel(logging.DEBUG)
        cls.file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )

        # add handlers
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().addHandler(cls.file_handler)
        
        # create composify logger
        composify_logger = logging.getLogger("composify")
        composify_logger.setLevel(logging.DEBUG)
        composify_logger.addHandler(cls.console_handler)
        composify_logger.addHandler(cls.file_handler)
        composify_logger.propagate = False

        # create interactions logger
        interactions_logger = logging.getLogger("interactions")
        interactions_logger.setLevel(logging.DEBUG)
        interactions_logger.addHandler(cls.console_handler)
        interactions_logger.addHandler(cls.file_handler)
        interactions_logger.propogate = False

        # create env logger
        env_logger = logging.getLogger("env")
        env_logger.setLevel(logging.DEBUG)
        env_logger.addHandler(cls.console_handler)
        env_logger.addHandler(cls.file_handler)
        env_logger.propogate = False

        # create build logger
        build_logger = logging.getLogger("build")
        build_logger = logging.setLevel(logging.DEBUG)
        build_logger.addHandler(cls.console_handler)
        build_logger.addHandler(cls.file_handler)
        build_logger.propogate = False

        # create db logger
        db_logger = logging.getLogger("db")
        db_logger.setLevel(logging.DEBUG)
        db_logger.addHandler(cls.file_handler)
        db_logger.propagate = False

    @classmethod
    def check_debug_logging(cls, debug):
        """
        * Set the logging level from 'INFO' to 'DEBUG' if True
        * Logs 'db' not only to file, but console as well.

        Args:
            debug (bool): set logging to debug or not? (e.g., True or False)
        """
        if debug:
            # Set the level for the console handler
            cls.console_handler.setLevel(logging.DEBUG)

        else:
            return
