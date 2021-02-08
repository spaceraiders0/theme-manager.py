"""The container for all the commands themer.py uses.
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parents[1]
THEMES_FOLDER = ROOT_DIR / Path("themes")
CACHE_FILE = ROOT_DIR / Path(".theme_cache")
SKELETON_FOLDER = THEMES_FOLDER / Path("skeleton")


def generate_tree():
    """Generates the needed files and folders.
    """

    SKELETON_INIT = SKELETON_FOLDER / Path("init.sh")
    SKELETON_DEINIT = SKELETON_FOLDER / Path("deinit.sh")

    if not CACHE_FILE.exists():
        open(CACHE_FILE, "x").close()

    if not THEMES_FOLDER.exists():
        THEMES_FOLDER.mkdir()

    if not SKELETON_FOLDER.exists():
        SKELETON_FOLDER.mkdir()
    
    if not SKELETON_INIT.exists():
        open(SKELETON_INIT, "x").close()

        with open(SKELETON_INIT, "w") as INIT_FILE:
            INIT_FILE.write("#!/usr/bin/env bash\n")

    if not SKELETON_DEINIT.exists():
        open(SKELETON_DEINIT, "x").close()

        with open(SKELETON_DEINIT, "w") as INIT_FILE:
            INIT_FILE.write("#!/usr/bin/env bash\n")


def new_theme(theme_name: str):
    """Generates a new theme if the skeleton folder exists.

    :param theme_name: the name of the theme
    :type theme_name: str
    """

    if SKELETON_FOLDER.exists():
        subprocess.run(["cp", "-r", str(SKELETON_FOLDER), str(THEMES_FOLDER / Path(theme_name))])
    else:
        print("Cannot generate new theme. No template theme.")


def display_theme():
    """Prints the current theme.
    """

    print(get_theme())


def get_theme() -> str:
    """Returns the current theme.

    :return: the current theme
    :rtype: str
    """

    with open(CACHE_FILE, "r") as cache_file:
        current_theme = cache_file.read().strip()

        return current_theme


def cache_theme(theme_name: str):
    """Caches the given theme.

    :param theme_name: the theme to cache
    :type theme_name: str
    """

    with open(CACHE_FILE, "w") as cache_file:
        cache_file.write(theme_name)


def validate_theme(theme_folder: Path) -> bool:
    """Validates that a theme is correctly constructed.
    A "correct" theme is a theme that has an init.sh,
    and deinit.sh file.

    :param theme_folder: the theme to validate
    :type theme_folder: Path
    :return: whether the files exist
    :rtype: bool
    """

    INIT = theme_folder / Path("init.sh")
    DEINIT = theme_folder / Path("deinit.sh")

    if INIT.exists() and DEINIT.exists():
        return True
    else:
        return False


def unload_theme():
    """Unloads the current theme if it is initialized.
    """
 
    current_theme = get_theme()

    # Make sure there is a loaded theme.
    if current_theme != "":
        # Make sure the loaded theme actualy exists.
        THEME_TO_UNLOAD = THEMES_FOLDER / Path(current_theme)
        DEINIT_FILE = THEME_TO_UNLOAD / Path("deinit.sh")

        if validate_theme(THEME_TO_UNLOAD):
            print(f"Unloading theme {current_theme}")
            subprocess.run(f"{DEINIT_FILE}")

            # Uncache the theme.
            open(CACHE_FILE, "w").close()
        else:
            print(f"Could not find deinit file for theme {current_theme}")
    else:
        print("No theme previously cached.")


def load_theme(theme_name: str):
    """Loads a theme from the themes folder. If there is a previously cached
    theme, and it exists in the themes folder, it will be deinitialized. If the
    provided theme is exists,

    :param theme_name: the theme to load
    :type theme_name: str
    """

    THEME_TO_LOAD = THEMES_FOLDER / Path(theme_name)
    INIT_FILE = THEME_TO_LOAD / Path("init.sh")

    if THEME_TO_LOAD.exists():
        unload_theme()

        # Make sure the theme to load actually exists.
        if validate_theme(THEME_TO_LOAD):
            print(f"Loading theme {theme_name}.")
            subprocess.run(f"{INIT_FILE}")
            cache_theme(theme_name)
        else:
            print(f"{theme_name} is missing init or deinit files.")
    else:
        print(f"{theme_name} is not a theme.")
        sys.exit(1)
