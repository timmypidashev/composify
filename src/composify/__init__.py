__title__ = "composify"
__summary__ = "Compose Project Manager"
__author__ = "Timothy Pidashev"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present Timothy Pidashev"
__version__ = "0.1.0"

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
    "verbose": False,
    "headless": False,
    "dev": False,
    "command": None,
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
    parser.add_argument("-d", "--dev", default=defaults["dev"], help=argparse.SUPPRESS, action="store_true")
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

async def run_as_module():
    # parse args
    await define_arguments()
    args = parser.parse_args()
    user_input = (vars(args))
    command = args.subcommand
    
    # Setup logging
    from . import log
    log = log.Logger("composify")
    log_path = log.configure_log_path(user_input["dev"])
    log.configure_handlers(log_path)
    log.check_debug_logging(user_input["verbose"])
    
    # Just some debug logging
    if user_input["dev"]:
        await log.debug("running in dev mode")

    # Setup db
    from . import db
    db = db.DB()
    await db.initialize(user_input["dev"])

    # Other internal imports go here
    from . import interactions

    if args.version:
        await log.info(f"{__title__} v{__version__}")
        sys.exit()

    elif command is None:
        await log.debug(f"command is none, defaulting to init")
        command = "init"

    # pass args to the proper interaction
    interactions = interactions.Interaction()
    interaction = getattr(interactions, command)
    await interaction(user_input, defaults)
