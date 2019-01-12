# PyMCL
PyMCL is a multimc-like (functionality wise) launcher for legacy minecraft versions (1.5.2 and lower).

It looks like the old beta launcher, but has the same features as many modern launchers.

## Features in Descending Order (priority)

 - [x] Fixed tumblr page.
 - [x] Themable for modpacks/personal needs.
 - [x] Extended options. (supports custom java args and ram limits right now)
 - [ ] Instancing.
 - [ ] Modpack manager. (somewhat similar to the twitch launcher)
 - [ ] Fixed login server. (Offline only atm)
 - [ ]  Discord integration. (shows what modpack you are playing and on what mc version)
 - [ ] Mod installer system similar to Nexus Mod Manager.
 - [ ] Stupidly lightweight.

## Compiling
**Requirements**:
You need Python 3, Pip 3, PyQt5, PyInstaller and AppDirs. (`pip3 install pyqt5 appdirs pyinstaller`)

**Usage**:
`python3 compile.py`
OR
 `pyinstaller -y -F -w -i favicon.ico --add-data "dirt.png":"." --add-data "favicon.png":"." --add-data "logo.png":"." launcher.py`. 

**Notes**:
 - If pyinstaller errors out with invalid syntax, use a semicolon (`;`)
   instead of a colon (`:`) in the `--add-data` arguments.
 - The compiled executable will be put in the dist folder when it is done.
 - To have a console for the launcher, remove the `-w` in the compile arguments when compiling.
 - The final file is *huge*. I recommend just using `python3 launcher.py` for personal use.
