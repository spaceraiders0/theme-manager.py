#!/usr/bin/env python

"""Installs the script by making a symlink.
"""

import os
import sys
import subprocess
from pathlib import Path

root_dir = Path(sys.argv[0]).parent.absolute()
executable = root_dir / Path("src/themer.py")

INSTALLATION_DIRECTORY = "/usr/local/bin"

# Prevents this script from being ran without root privileges.
if os.environ["USER"] != "root":
    print("This script needs to be executed using root privileges.")
    sys.exit(1)

try:
    subprocess.run(["ln", "-s", str(executable), INSTALLATION_DIRECTORY])
except subprocess.CalledProcessError:
    print("Installation was unsuccessful.")
