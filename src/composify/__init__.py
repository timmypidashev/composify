__title__ = "composify"
__summary__ = "Compose Project Manager"
__author__ = "Timothy Pidashev"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present Timothy Pidashev"
__version__ = "0.1.0"

from . import interactions
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
    "verbose": False,
    "command": "init",
    "project_name": None
}

# Use the custom formatter
parser = argparse.ArgumentParser(
    prog=__title__,
    description=__summary__,
    usage=argparse.SUPPRESS
)

async def define_arguments():
    """
    Define command-line arguments.
    """
    # top level args
    parser.add_argument("-v", "--version", default=defaults["version"], help="output version information and exit", action="store_true")
    parser.add_argument("-vv", "--verbose", default=defaults["verbose"], help="run with verbose output shown", action="store_true")
    # TODO: Add hidden dev arg with argparse.SUPPRESS

    # subparsers
    subparsers = parser.add_subparsers(title="commands", dest='subcommand')
    
    # init subparser and args
    init_parser = subparsers.add_parser("init", help="initialize a new project")
    init_parser.add_argument("project_name", type=str, nargs="?", default=defaults["project_name"], help="the name of the project")

    # build subparser and args
    build_parser = subparsers.add_parser("build", help="build project")

    # run subparser and args
    run_parser = subparsers.add_parser("run", help="run project")

    # bump subparser and args
    bump_parser = subparsers.add_parser("bump", help="bump project version")

    # push subparser and args
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

    # command args
    command = args.subcommand
    interaction = getattr(interactions, command)

    return user_input, interaction

async def run_as_module():
    await db.build()
    await define_arguments()
    user_input, interaction = await parse_arguments()
    await interaction(user_input, defaults)
