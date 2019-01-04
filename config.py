import appdirs, os, sys
TEST_URL="http://google.cn/generate_204" # to be hardcoded.
NAME="Minecraft"
BOTTOM_BACKGROUND="dirt.png" # to be removed for theming support.
LOGO="logo.png" # to be removed for theming support.
ICON="favicon.png" # to be removed for theming support.
UPDATE_URL="https://github.com/calmilamsy/b1.7.3_minecraft_launcher/raw/master/version.json"

##version.json:
##    Should have this format:
##        {
##            "version": "1.0",
##            "method": "mediafire",
##            "link": "b1y22baktdkqhRY"
##        }

#
# NOTES:
#    NAME:
#       The name you want for the launcher.
#    UPDATE_URL:
#        Rawfile:
#            The url to your version.json file. (e.g: "https://github.com/user/project/raw/master/version.json")
#
# VERSION.JSON:
#    Version:
#        The modpack version. If the modpack version is LOWER than the remote version, then the modpack will be downloaded. Only FLOATS OR INTEGERS.
#    Method:
#        Mediafire:
#            A mediafire folder ID. (e.g. b1y22baktdkqhRY)
#        Rawfile:
#            Any link that directly gives a zip, 7z or rar file as response. (e.g: "https://github.com/user/project/raw/master/modpack.zip")
#    Link:
#        Anything that isnt a zip, 7z or rar file will be put in .minecraft.
#        Mediafire:
#            A mediafire folder ID.
#        Rawfile:
#            Any link that directly gives a zip, 7z or rar file as response.

# DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING

DEFAULT_CONFIG="""
{
    "maxram": "256m",
    "minram": "256m",
    "javaargs": "",
    "lastusedname": ""
}
"""

VER="Launcher v0.1 Alpha"

MC_DIR=appdirs.user_data_dir(".minecraft", "", roaming=True)