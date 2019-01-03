import appdirs, os, sys
MC_DIR=appdirs.user_data_dir(".minecraft", "", roaming=True)
TEST_URL="http://google.cn/generate_204"
NAME="Minecraft Launcher"
VER="v0.1 Alpha"
PLAYERNAME="TEST"
BOTTOM_BACKGROUND="dirt.png"
LOGO="logo.png"
ICON="favicon.png"
UPDATE_URL="https://github.com/calmilamsy/b1.7.3_minecraft_launcher/raw/master/version.json" # github link to the version.json file.

##version.json:
##    Should have this format:
##        {
##            "version": "1.0",
##            "method": "mediafire", OR "github"
##            "link": "b1yv2baktdkqhry (the stuff after /file/ but before /modpack.zip in the url)" OR "https://github.com/user/project/raw/master/modpack.zip (supports any url that gives the modpack file directly as response.)"
##        }