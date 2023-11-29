__title__ = "composify"
__summary__ = "Compose Project Manager"
__author__ = "Timothy Pidashev"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present Timothy Pidashev"
__version__ = "0.1.0"

import argparse
import sys


"""
Composify argument defaults dict and
the user defined arguments dict.
"""
defaults = {
    "verbose": False, 
    "version": False
}
arguments = dict()

class HelpFormatter(argparse.HelpFormatter):
    """
    Custom argparse help formatter. Currently this allows for the following:
    - Disables metavar for short args. Example without(-t {usb, iso} --type {usb, iso}) | Example with(-t --type {usb, iso})
    - Allows for extending the default column size for help variables.
    """
    def __init__(self, prog):
        super().__init__(prog, max_help_position=40, width=80)

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

format = lambda prog: HelpFormatter(prog)

parser = argparse.ArgumentParser(
    prog=__title__,
    usage='%(prog)s [options]',
    description=__summary__,
    formatter_class=format
)


def define_arguments():
    """
    Define command-line arguments.
    """
    parser.add_argument("-vv", "--verbose", default=defaults["verbose"], help="set composify output to output debug logs", action="store_true") 
    parser.add_argument('-v', '--version', default=defaults["version"], help='output version information and exit', action='store_true')


def parse_arguments():
    """
    Parse arguments. If none inputted, default to '--help'.
    """
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.version:
        print(f'{__title__} v{__version__}')

    # Set verbosity level of traceback
    # set_verbosity_level(arguments['verbose'])

    

def run_as_module():
    
    define_arguments()
    parse_arguments()
