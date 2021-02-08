#!/usr/bin/env python

import sys
import definitions
from pathlib import Path
from argparse import ArgumentParser

commands = {
    "display-theme": definitions.display_theme,
    "unload-theme": definitions.unload_theme,
    "load-theme": definitions.load_theme,
    "new-theme": definitions.new_theme,
}

# Generate required files.
definitions.generate_tree()

ThemerParser = ArgumentParser(description="""A theme manager for Linux.""")
ThemerParser.add_argument("action")
ThemerParser.add_argument("subcommands", nargs="*")
themer_args = ThemerParser.parse_args()

# Load and execute the command.
for command_name, command_func in commands.items():
    if command_name == themer_args.action:
        try:
            command_func(*themer_args.subcommands)
            sys.exit(0)
        except TypeError:
            print(f"{len(themer_args.subcommands)} is an invalid number of arguments.")
            sys.exit(1)
else:
    print(f"'{themer_args.action}' is an invalid action.")
    sys.exit(1)
