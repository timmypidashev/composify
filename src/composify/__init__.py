__title__ = "composify"
__summary__ = "Compose Project Manager"
__author__ = "Timothy Pidashev"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present Timothy Pidashev"
__version__ = "0.1.0"


from . import db
from . import log
from . import errors

import asyncio
import argparse
import sys
import os


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
    args = parser.parse_args()

    # Remove specific options before displaying help
    #if args.version:
    #    print(f'{__title__} v{__version__}')


async def create_config_dir():
    """
    Create '/etc/composify' if the folder doesn't yet exist
    """
    # TODO: reimplement with an os agnostic approach
    # NOTE: this function will be replaced soon by a 'system' module!

    user_home = os.path.expanduser("~")
    config_path = os.path.join(user_home, ".config", "composify")

    try:
        # Check if the directory exists, and create it if not
        if not os.path.exists(config_path):
            os.makedirs(config_path)

    except Exception:
        print("Only posix based systems are supported at the moment!")
    

def run_as_module():
    asyncio.run(create_config_dir())
    asyncio.run(define_arguments())
    asyncio.run(parse_arguments())
