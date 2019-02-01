import sys
import config
from PyQt5.QtGui import QPixmap
from json import loads, dumps
from os.path import exists, dirname, abspath


def resourcePath(relative_path):
    base_path = getattr(sys, '_MEIPASS', dirname(abspath(__file__)))
    return base_path + "/" + relative_path


def loadImage(relative_path):
    try:
        if not exists(config.MC_DIR + "/theme/" + relative_path):
            print("No Theme")
            raise IOError
        img = QPixmap(config.MC_DIR + "/theme/" + relative_path)
    except IOError:
        img = QPixmap(resourcePath(relative_path))

    return img


def loadSettings(mainWindow):
    if not exists(config.MC_DIR):
        # noinspection PyCallByClass,PyTypeChecker
        mainWindow.error("Missing Minecraft directory. Is minecraft installed?")
        makedirs(config.MC_DIR + "/.minecraft")
    if not exists(config.MC_DIR + "/launcher_config.json"):
        file = open(config.MC_DIR + "/launcher_config.json", "w")
        file.write(config.DEFAULT_CONFIG)
        file.close()
    file = open(config.MC_DIR + "/launcher_config.json", "r")
    launcherConfig = loads(file.read())
    file.close()

    return launcherConfig


def saveSettings(launcherConfig):
    file = open(config.MC_DIR + "/launcher_config.json", "w")
    file.write(dumps(launcherConfig, indent=4, sort_keys=True))
    file.close()
