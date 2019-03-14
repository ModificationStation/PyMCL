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

DEFAULT_LAUNCHER_CONFIG = """
{
    "lastusedname": ""
}
"""

DEFAULT_INSTANCE_CONFIG = """
{
    "maxram": "512m",
    "minram": "256m",
    "javaargs": ""
}
"""

VER = "v0.6 Alpha Pre 1"


if platform.platform().startswith("Windows"):
    MC_DIR = os.getenv("APPDATA") + "/.PyMCL"
    OS = "windows"
elif platform.platform().startswith("Darwin"):
    MC_DIR = os.path.expanduser("~") + "/Library/Application Support/PyMCL"
    OS = "osx"
else:
    MC_DIR = os.path.expanduser("~") + "/.PyMCL"
    OS = "linux"
