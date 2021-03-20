#!/usr/bin/env python

import sys
import definitions
from argparse import ArgumentParser

theme_controller = definitions.ThemeManager()
commands = {
    "get-theme": theme_controller.get_last_theme,
    "get-colors": theme_controller.get_colors,
    "get-path": theme_controller.get_theme_folder,
    "get-controls": theme_controller.get_controls,
    "unload-theme": theme_controller.unload_theme,
    "load-theme": theme_controller.load_theme,
    "new-theme": theme_controller.new_theme,
}

themer_parser = ArgumentParser(description="A theme manager for Linux.")
themer_parser.add_argument("action")
themer_parser.add_argument("subcommands", nargs="*")
themer_args = themer_parser.parse_args()

# Load and execute the command.
for command_name, command_func in commands.items():
    if command_name == themer_args.action:
        try:
            output = command_func(*themer_args.subcommands)

            if output is not None:
                if isinstance(output, (list, tuple)):
                    print("\n".join(map(str, output)))
                else:
                    print(str(output))

            sys.exit(0)
        except TypeError:
            print(f"{len(themer_args.subcommands)} is an invalid number of arguments.")
            sys.exit(1)
else:
    print(f"'{themer_args.action}' is an invalid action.")
    sys.exit(1)
