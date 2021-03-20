#!/usr/bin/env python

"""Installs the script by making a symlink.
"""

import os
import sys
import subprocess
from pathlib import Path
from argparse import ArgumentParser

root_dir = Path(sys.argv[0]).parent.absolute()
EXECUTABLE_PATH = root_dir / Path("src/themer.py")
INSTALLATION_DIRECTORY = Path("/usr/local/bin")

install_parser = ArgumentParser(description="Installs a script.")
install_parser.add_argument("-i", "--install", action="store_true",
                            help="Installs the script.")
install_parser.add_argument("-u", "--uninstall", action="store_true",
                            help="Uninstalls the script.")
install_parser.add_argument("-t", "--target", default=INSTALLATION_DIRECTORY,
                            help="Changes the installation directory.",
                            metavar="t")
install_args = install_parser.parse_args()

# Prevents this script from being ran without root privileges.
if os.environ["USER"] != "root":
    print("This script needs to be executed using root privileges.")
    sys.exit(1)

try:
    location = str(install_args.target)

    if install_args.install is True:
        print(f"Symlinking {str(EXECUTABLE_PATH)} to {location}")
        code = subprocess.run(["ln", "-s", str(EXECUTABLE_PATH), location],
                              stderr=subprocess.DEVNULL)

        if code == 0:
            print("Installation complete.")
        else:
            print("Installation failed.")
    else:
        print(f"Removing symlink pointing to {str(EXECUTABLE_PATH)} from {location}")
        code = subprocess.run(["rm", f"{location}/{EXECUTABLE_PATH.name}"],
                              stderr=subprocess.DEVNULL)

        if code == 0:
            print("Uninstallation was successful.")
        else:
            print("Uninstalltion was unsuccessful.")
except subprocess.CalledProcessError:
    print("Installation was unsuccessful.")
