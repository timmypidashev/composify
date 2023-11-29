# system
import os
import sys
import yaml
import asyncio
import traceback
from dotenv import load_dotenv
import logging
import logging.config
import coloredlogs

# configure logging
with open("./composify/log_config.yaml",  "r") as file:
    configuration = yaml.safe_load(file.read())
    logging.config.dictConfig(configuration)

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
