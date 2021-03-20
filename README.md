# theme-manager.py
theme-manager is an application to manage Linux themes. It provides the base utilities of generating, and loading
new themes.

## How does it work?
This revolves around "themes." A theme has an ``init.sh`` file, and a ``deinit.sh`` file. These are required, or else
the script will not be able to "load" the theme. The ``init.sh`` file is basically a collection of commands that start
processes, move files, etc. The ``deinit`` file reverses these changes. There is also an optional ``colors`` file, which
contains color information used by the theme. This is mainly just for external programs.

## Installation
Installation is quite simple. To start, go to a directory where you would like to store the script, and run the following
command in your terminal:
```bash
$ git clone https://github.com/spaceraiders0/theme-manager.py
```
Then..
```bash
$ cd theme-manager.py/
```
Then..
```bash
$ ./install.py -i
```
And that is all you must do. You can then execute the script from anywhere you would like.

## Uninstallation
Uninstallation is also quite simple. Simply go to the root directory of the application, and run the following command:
```bash
$ ./install.py -u
```
And the script should be automatically removed.

## Basic Usage
Assuming you have followed the installation steps above, you may want to create your own "theme." To get started, execute
the following command in your shell:
```
$ themer.py new-theme theme_name_here
```
That will create a new skeleton / template theme in the new ``themes`` directory. To begin making your theme, navigate to
the new directory, and edit the ``init.sh`` file. There, you can put any commands that should be executed to replicate your
current layout. You should also edit the ``deinit.sh`` file, which should scripted to reverse the actions done by the
``init.sh`` file. From here, you can now do:
```bash
$ themer.py load-theme theme_name
```
To load your theme. This will also automatically unload any theme that is already loaded, so you do not need to do it manually.
```bash
$ themer.py unload-theme
```
To unload your currently loaded theme. 
</br></br>
You can also edit the ``colors.txt`` file, which will allow the color information of your theme to be read by external
programs using the following command:
```bash
$ themer.py get-colors
```

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
