"""The container for all the commands themer.py uses.
"""

import subprocess
from pathlib import Path

root_dir = Path(__file__).parent.parent
themes_folder = root_dir / Path("themes")
cache_file = root_dir / Path(".theme_cache")
skeleton_folder = themes_folder / Path("skeleton")
file_structure = {
    ".theme_cache": None,
    "themes": {
        "skeleton": {
            "deinit.sh": "#!/usr/bin/env bash\n\n",
            "init.sh": "#!/usr/bin/env bash\n\n",
            "colors.txt": None,
        }
    }
}


class NoThemeControlsError(Exception):
    pass


class ThemeNotFoundError(Exception):
    pass


class ThemeManager():
    def __init__(self, theme_folder_overwrite: Path = themes_folder):
        # Initialize the file structure.
        for new_path, is_dir in self._iter_structure(root_dir, file_structure):
            if new_path.exists() is False:
                if is_dir is True:
                    new_path.mkdir()
                else:  # Write default text.
                    with open(new_path, "w+") as file_buffer:
                        if isinstance(is_dir, str):
                            file_buffer.write(is_dir)

        themes_folder = theme_folder_overwrite 

        if themes_folder.exists() is False:
            raise ValueError("Themes folder does not exist.")



    @staticmethod
    def _iter_structure(root: Path, structure: dict) -> (Path, bool):
        """Iterates through a given structure and yields the path
        to a folder, or file based off a root directory.

        :param root: the root directory to start based off
        :type root: Path
        :param structure: the dictionary to parse
        :type structure: dict
        :return: a Path to a file or folder, and whether or not
                it is a folder
        :rtype: Path, bool
        """

        folders = [(structure, root)]

        while len(folders) > 0:
            sub_folder, path_to = folders.pop(0)

            # Yield paths and add more sub-folders.
            for name, descendants in sub_folder.items():
                new_path_to = path_to / Path(name)
                is_folder = isinstance(descendants, dict)

                # New folder to loop through.
                if is_folder:
                    folders.append((descendants, new_path_to))
                else:  # Usually for returning text for a file.
                    is_folder = descendants

                yield new_path_to, is_folder

    @staticmethod
    def get_theme_folder(theme_name: str) -> Path:
        """Retrieves the folder of the theme provided.

        :param theme_name: the name of the theme to retrieve
        :type theme_name: str
        """

        theme_path = themes_folder / Path(theme_name)

        if theme_path.exists() is True:
            return theme_path
        else:
            return None

    @staticmethod
    def _validate_theme(theme_folder: Path) -> bool:
        """Returns whether or not a theme folder is valid. A "valid" folder
        is defined as a folder that contains both an init, and a deinit file.

        :param theme_folder: the path to the theme's folder
        :type theme_folder: Path
        :return: whether or not the folder is valid
        :rtype: bool
        """

        has_init = (theme_folder / Path("init.sh")).exists()
        has_deinit = (theme_folder / Path("deinit.sh")).exists()

        return has_init and has_deinit

    @staticmethod
    def get_last_theme() -> str:
        """Returns the name of the previous theme, if there was one.
        """

        try:
            with open(cache_file, "r") as cache_buffer:
                last_theme = cache_buffer.read()

                if len(last_theme) > 0:
                    return last_theme.strip("\n")
        except FileNotFoundError:
            pass

        return None

    def get_colors(self, theme_folder: (Path, str)) -> list:
        """Retrieves the colors used by a theme if a colors file exists.

        :param theme_folder: the folder or name of the theme to get color
                information from
        :type theme_folder: Path, str
        :return: a list of colors from the colors file
        :rtype: list
        """

        # Try to find path to the theme based off it's name.
        if isinstance(theme_folder, str):
            theme_folder = self.get_theme_folder(theme_folder)

        colors_file = theme_folder / Path("colors.txt")

        if colors_file.exists() is False:
            return []

        # Retrieve all the colors
        colors = []

        with open(colors_file, "r") as colors_buffer:
            for color in map(str.strip, colors_buffer.readlines()):
                if len(color) > 0:
                    colors.append(color.strip("\n"))

        return colors

    def get_controls(self, theme_to_load: (Path, str)) -> (Path, Path):
        """Returns the paths to the init, and deinit files of a theme.

        :param theme_to_load: the theme folder or name of the theme to retrieve
                the controls of.
        :type theme_to_load: Path, str
        :return: the Paths to both the init, and deinit files.
        :rtype: Path, Path
        """

        # Try to find path to the theme based off it's name.
        if isinstance(theme_to_load, str):
            theme_to_load = self.get_theme_folder(theme_to_load)


        # Make sure that the folder is valid.
        if self._validate_theme(theme_to_load) is False:
            return None, None

        return theme_to_load / Path("init.sh"), theme_to_load / Path("deinit.sh")

    def unload_theme(self):
        """Unloads the currently loaded theme.
        """

        previous_theme = self.get_theme_folder(self.get_last_theme())

        # Deinitialize the previous theme if there was one defined.
        if previous_theme is not None:
            if self._validate_theme(previous_theme) is True:
                init, deinit = self.get_controls(previous_theme)

                subprocess.call(f"{str(deinit)}")

                # Empty the theme cache file
                open(cache_file, "w").close()

    def load_theme(self, theme_to_load: str):
        """Attempts to load a theme.

        :param theme_to_load: the name of the theme
        :type theme_to_load: str
        """

        next_theme = self.get_theme_folder(theme_to_load)

        # Do not want to deinitialize the current theme if none does not
        # already exist
        if next_theme is None:
            raise ThemeNotFoundError(f"{theme_to_load} is not a defined theme.")

        if self._validate_theme(next_theme) is False:
            raise NoThemeControlsError(f"{theme_to_load} is a malformed theme.")

        self.unload_theme()

        # Initialze the next theme.
        init, deinit = self.get_controls(next_theme)
        subprocess.call(f"{str(init)}")

    def new_theme(self, new_theme_name: str) -> str:
        """Creates a new template theme with a certain name.

        :param new_theme_name: the name of the new theme
        :type new_theme_name: str
        :return: status message
        :rtype: str
        """

        new_structure = {
            new_theme_name: file_structure["themes"]["skeleton"].copy()
        }

        if self.get_theme_folder(new_theme_name) is not None:
            return "Theme already exists."
        
        # Create the new theme.
        for new_path, is_dir in self._iter_structure(themes_folder, new_structure):
            if new_path.exists() is False:
                if is_dir is True:
                    new_path.mkdir()
                else:  # Write default text.
                    with open(new_path, "w+") as file_buffer:
                        if isinstance(is_dir, str):
                            file_buffer.write(is_dir)

        return "Created theme!"
