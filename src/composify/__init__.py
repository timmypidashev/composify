__title__ = "composify"
__summary__ = "Compose Project Manager"
__author__ = "Timothy Pidashev"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present Timothy Pidashev"
__version__ = "0.1.0"

from . import errors
from . import log
from . import db

import asyncio
import argparse
import sys
import os

log = log.Logger("composify")

"""
Composify argument defaults dict and
the user defined arguments dict.
"""
defaults = {
    "version": False,
    "debug": False
}
arguments = dict()

# Use the custom formatter
parser = argparse.ArgumentParser(
    add_help=False  # Disable automatic help display for the main parser
)

async def define_arguments():
    """
    Define command-line arguments.
    """
    
    # commands
    subparsers = parser.add_subparsers(dest='subcommand')
    init = subparsers.add_parser("init",)

async def help_message():
    #TODO: Literally print a help command instead of relying on argparse
    pass


async def parse_arguments():
    """
    Parse arguments. If none inputted, default to '--help'.
    """
    await log.debug(f"Running version {__version__}")

    args = parser.parse_args()

    await log.info("test")

    # Remove specific options before displaying help
    #if args.version:
    #    print(f'{__title__} v{__version__}')

def run_as_module():
    asyncio.run(define_arguments())
    asyncio.run(parse_arguments())
