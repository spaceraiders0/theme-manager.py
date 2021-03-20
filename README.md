# theme-manager.py
theme-manager is an application to manage Linux themes. It provides the base utilities of generating, and loading
new themes.

## How does it work?
This revolves around "themes." A theme has an ``init.sh`` file, and a ``deinit.sh`` file. These are required, or else
the script will not be able to "load" the theme. The ``init.sh`` file is basically a collection of commands that start
processes, move files, etc. The ``deinit`` file reverses these changes. There is also an optional ``colors`` file, which
contains color information used by the theme. This is mainly just for external programs.

## Installation
To install, simply run the script ``install.py -i`` with sudo privileges. The main script is symlinked to ``/usr/local/bin/``
by default, but can be changed. Uninstalling the script can be done using ``install.py -u``

## Commands
There are a few commands packaged with this program. They are:

```
get-theme: returns the name of the currently loaded theme
get-colors: returns the colors of a theme
get-path: returns the path of a theme
get-controls: returns the init.sh and deinit.sh files of a theme.
load-theme: loads the a new theme, and unloads the previously loaded theme.
unload-theme: unloads the current theme.
new-theme: creates a new skeleton theme with a name.
```
