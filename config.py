import os
import platform

# DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING.

NAME = "PyMCL"
ICON = ""
LOGO = ""
BACKGROUND = ""
UPDATE_URL = "https://github.com/ModificationStation/PyMCL/raw/master/version.json"
MODPACK_DB = "https://github.com/ModificationStation/PyMCL/raw/master/modpacks.json"
BLOG_BACKGROUND = "blogbackground.png"
BLOG = ""

# THIS IS IN JSON, NOT PYTHON
DEFAULT_LAUNCHER_CONFIG = """
{
    "lastusedname": ""
}
"""

# THIS IS IN JSON, NOT PYTHON
DEFAULT_INSTANCE_CONFIG = """
{
    "maxram": "512m",
    "minram": "256m",
    "javaargs": "",
    "proxyskin": false,
    "proxysound": false,
    "proxycape": false
}
"""

VER = "v0.6 Alpha Pre 3"

# Sets minecraft install dir. DO NOT TOUCH UNLESS YOU KNOW WHAT YOU ARE DOING.
# Touching this can cause unintended file deletion/overwrites/etc.
# I have tried to mitigate the risks, but seriously, NO TOUCHIE
if platform.platform().startswith("Windows"):
    MC_DIR = os.getenv("APPDATA") + "/.PyMCL"
    OS = "windows"
elif platform.platform().startswith("Darwin"):
    MC_DIR = os.path.expanduser("~") + "/Library/Application Support/PyMCL"
    OS = "osx"
else:
    MC_DIR = os.path.expanduser("~") + "/.PyMCL"
    OS = "linux"
