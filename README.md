# PyMCL
PyMCL is a multimc-like (functionality wise) launcher for legacy minecraft versions (1.5.2 and lower).

It looks like the old beta launcher, but has the same features as many modern launchers.

## Features in Descending Order (priority)
This list is based off of the old beta launcher.

 - [x] Fixed tumblr page.
 - [x] Themable for modpacks/personal needs.
 - [x] Extended options. (supports custom java args and ram limits right now)
 - [x] Instancing.
 - [x] Modpack manager. (somewhat similar to the twitch launcher)
 - [x] Fixed login. (still offline for now, but will fetch username from credentials)
 - [ ] Discord integration. (shows what modpack you are playing and on what mc version)
 - [ ] Mod installer system similar to Nexus Mod Manager.
 - [ ] Stupidly lightweight.

## Compiling 
##### You need Python 3.6+ (made on 3.7.2)
This assumes that you know the basics of script execution on your OS.

**Requirements If Pyinstalling Manually**:
___USE A VIRTUAL ENVIRONMENT___ (`python -m venv venv`) then (`venv/Scripts/activate`)
Pip 3, PyQt5, PyInstaller, Requests and AppDirs. (`pip3 install pyqt5 appdirs pyinstaller requests`)


##### Automated Compile:
Run the batch/shell file for your OS.
___Linux/macos script is untested___

##### Manual Compile:
 `pyinstaller -y -F -w -i favicon.ico --add-data "background.png":"." --add-data "favicon.ico":"." --add-data "logo.png":"." launcher.py`.

**Notes**:
 - If pyinstaller errors out with invalid syntax, use a semicolon (`;`)
   instead of a colon (`:`) in the `--add-data` arguments.
 - The compiled executable will be put in the dist folder when it is done.
 - To have a console for the launcher, remove the `-w` in the compile arguments when compiling.
 - The final file is pretty big. (~80mb)
