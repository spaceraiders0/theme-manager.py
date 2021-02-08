# theme-manager.py
theme-manager is an application to manage Linux themes.
It provides the base utilities of generating, and loading
new themes.

## Commands
There are a few commands packaged with this program. They are:
```
display-theme - Prints the current theme.
unload-theme - Unloads the current theme by calling the deinit
               file in the currently loading theme's directory.
load-theme <theme-name> - Loads a theme. Calls the init file in
                          theme's directory.
new-theme <theme-name> - Generates a new theme template based off
                         of a name.
```
