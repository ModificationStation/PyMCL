# PyMCL
PyMCL is a multimc-like (functionality wise) launcher for legacy minecraft versions (1.5.2 and lower).

It looks like the old beta launcher, but has the same features as many modern launchers.

## Features in Descending Order (priority)
This list is based off of the old beta launcher.  
[Changelog](https://github.com/ModificationStation/PyMCL/blob/master/changelog.md)

 - [x] Fixed tumblr page.
 - [x] Themable for modpacks/personal needs.
 - [x] Extended options. (supports custom java args and ram limits right now)
 - [x] Instancing.
 - [x] Modpack manager.
 - [x] Fixed login.
 - [x] Discord integration.
 - [x] MultiMC instance support.
 - [ ] Mod installer system similar to Nexus Mod Manager.
 - [ ] Stupidly lightweight.

## Compiling
**You need Python 3.6+ (made on 3.7.2)**  
This assumes that you know the basics of script execution and dependency resolving on your OS.  

##### Automated Compile:
Run the batch/shell file for your OS.  

**OSX**:  
Unix script works on OSX.  
You will need to install pip and virtualenv first though.  
Edit the script to use your python 3.6+ install and run it.

**\*Unix**:  
Should work. Untested.  
Some distros come with python 2.7 installed. This uses python 3.6+, so install that.  
Edit the script to use your python 3.6+ install and run it.  

**Windows Vista+**:  
Just run the compile script.

##### Manual Compile:
___USE A VIRTUAL ENVIRONMENT___  
(`python -m venv venv`) then (`venv/Scripts/activate`)  

get Pip 3, PyQt5, PyInstaller, Requests and AppDirs. (`pip3 install pyqt5 appdirs pyinstaller requests`)  
Then use pyinstaller on the launcher:  
 `pyinstaller -y -F -w -i favicon.ico --add-data "background.png":"." --add-data "favicon.ico":"." --add-data "logo.png":"."  --add-data "blogbackground.png":"."  --add-data "blog.html":"." launcher.py`.

**Notes**:
 - If pyinstaller errors out with invalid syntax, use a semicolon (`;`)
   instead of a colon (`:`) in the `--add-data` arguments.
 - The compiled executable will be put in the dist folder when it is done.
 - To have a console for the launcher, remove the `-w` in the compile arguments when compiling.
 - The final file is pretty big. (~40mb)
