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
    "verbose": False
}
arguments = dict()

# Use the custom formatter
parser = argparse.ArgumentParser(
    #add_help=False  # Disable automatic help display for the main parser
)

async def define_arguments():
    """
    Define command-line arguments.
    """
    # args
    parser.add_argument("-v", "--version", default=defaults["version"], help="output version information and exit", action="store_true")
    parser.add_argument("-vv", "--verbose", default=defaults["verbose"], help="run with verbose output", action="store_true")

    # subparser args
    subparsers = parser.add_subparsers(dest='subcommand')
    init_parser = subparsers.add_parser("init", help="initialize a new project")
    build_parser = subparsers.add_parser("build", help="build project")
    run_parser = subparsers.add_parser("run", help="run project")
    bump_parser = subparsers.add_parser("bump", help="bump project version")
    push_parser = subparsers.add_parser("push", help="push image")

async def parse_arguments():
    """
    Parse arguments. If none inputted, default to '--help'.
    """
    args = parser.parse_args()
    
    # Add argparse options to dict(user_input)
    user_input = (vars(args))

    # Determine if log level should be 'DEBUG' or 'INFO'
    log.check_debug_logging(user_input["verbose"])

    # Remove specific options before displaying help
    if args.version:
        await log.info(f'{__title__} v{__version__}')
        sys.exit()

    await log.debug(f"Running version {__version__}")

def run_as_module():
    asyncio.run(db.build())
    asyncio.run(define_arguments())
    asyncio.run(parse_arguments())
