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
    help_parser = subparsers.add_parser("help")
    init_parser = subparsers.add_parser("init")
    build_parser = subparsers.add_parser("build")
    run_parser = subparsers.add_parser("run")
    bump_parser = subparsers.add_parser("bump")
    push_parser = subparsers.add_parsers("push")

async def help_message():
    print(f"{__title__} ({__summary__}) v{__version__}")
    print("")
    print("Commands:")
    print("init:       initialize a new project")
    print("build:      build project")
    print("run:        run project"
    print("bump:       bump project version")
    print("push:       push image")

async def parse_arguments():
    """
    Parse arguments. If none inputted, default to '--help'.
    """
    await log.debug(f"Running version {__version__}")

    args = parser.parse_args()

    if args.subcommand == "help":
        await help_message()
        return

    await log.info("test")

    # Remove specific options before displaying help
    #if args.version:
    #    print(f'{__title__} v{__version__}')

def run_as_module():
    asyncio.run(db.build())
    asyncio.run(define_arguments())
    asyncio.run(parse_arguments())
