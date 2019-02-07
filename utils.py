import sys
import config
import requests
import shutil
from PyQt5.QtGui import QPixmap
import json
import zipfile
import os
import io
import urllib
from distutils.dir_util import copy_tree, remove_tree

from PyQt5.QtWidgets import QMessageBox


def resourcePath(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return base_path + "/" + relative_path


def loadImage(relative_path, instanceName=""):
    if not os.path.exists(config.MC_DIR + "/instances/" + instanceName + "/theme/" + relative_path):
        img = QPixmap(resourcePath(relative_path))
    else:
        img = QPixmap(config.MC_DIR + "/instances/" + instanceName + "/theme/" + relative_path)
    return img


def loadSettings():
    if not os.path.exists(config.MC_DIR + "/launcher_config.json"):
        file = open(config.MC_DIR + "/launcher_config.json", "w")
        file.write(config.DEFAULT_CONFIG)
        file.close()
    file = open(config.MC_DIR + "/launcher_config.json", "r")
    launcherConfig = json.loads(file.read())
    file.close()

    return launcherConfig


def saveSettings(launcherConfig):
    file = open(config.MC_DIR + "/launcher_config.json", "w")
    file.write(json.dumps(launcherConfig, indent=4, sort_keys=True))
    file.close()

def login(username, password):
    data = {
        "agent": {
            "name": "Minecraft",
            "version": 1
        },
        "username": username,
        "password": password,
        "requestUser": False
    }

    data = requests.post("https://authserver.mojang.com/authenticate", json=data)
    data = json.loads(data.content)

    try:
        return data["selectedProfile"]["name"]
    except AttributeError:
        return False

def checkOnline():
    try:
        reqests.get("http://google.com/generate_204")
        return True
    except:
        return False


def getModpacks():
    data = requests.get(config.UPDATE_URL)
    return data


def areYouThere(path):
    if not os.path.exists(path):
        os.makedirs(path)


def getModpackURL(modpackURL):
    if not os.path.exists(config.MC_DIR+"/modpackzips/"):
        os.makedirs(config.MC_DIR+"/modpackzips/")
    modpackName = urllib.parse.unquote_plus(modpackURL.rsplit('/', 1)[-1].split(".")[0])
    print(modpackName)

    if os.path.exists(config.MC_DIR + "/modpackzips/" + modpackName + ".zip"):
        print("Using cached file.")
    else:
        print("Attempting download")
        try:
            response = requests.get(modpackURL, stream=True)
            with io.open(config.MC_DIR + "/modpackzips/" + modpackName + ".zip", 'wb') as fd:
                for chunk in response.iter_content(chunk_size=4096):
                    fd.write(chunk)
        except:
            modpackName = "Error"
    return modpackName


def getModapackFS(modpackDir):
    try:
        if not os.path.exists(config.MC_DIR+"/modpackzips/"):
            os.makedirs(config.MC_DIR+"/modpackzips/")
        modpackName = os.path.splitext(os.path.basename(modpackDir))[0]
        if os.path.exists(config.MC_DIR + "/modpackzips/" + modpackName + ".zip"):
            os.remove(config.MC_DIR + "/modpackzips/" + modpackName + ".zip")
        shutil.copy(modpackDir, config.MC_DIR + "/modpackzips/"+modpackName + ".zip")
    except:
        modpackName = "Error"
    return modpackName


def installModpack(modpackName):
    print("Installing Modpack")
    try:
        if modpackName == "Error":
            raise IOError("Modpack does not exist in directory?")
        if not os.path.exists(config.MC_DIR + "/tmp/" + modpackName):
            os.makedirs(config.MC_DIR + "/tmp/" + modpackName)

        zip = zipfile.ZipFile(config.MC_DIR + "/modpackzips/" + modpackName + ".zip", "r")
        zip.extractall(config.MC_DIR + "/tmp/" + modpackName)
        zip.close()
        try:
            with open(config.MC_DIR + "/tmp/" + modpackName + "/.minecraft/modpack.json", "r") as file:
                modpackJson = json.loads(file.read())
                modpackJsonName = modpackJson["modpackname"]
        except:
            print("No modpack name found. Using zip file name.")
            modpackJsonName = modpackName

        if not os.path.exists(config.MC_DIR + "/instances/" + modpackJsonName):
            os.makedirs(config.MC_DIR + "/instances/" + modpackJsonName)

        copy_tree(config.MC_DIR + "/tmp/" + modpackName, config.MC_DIR + "/instances/" + modpackJsonName)
        print("Finding Readmes")
        files = [f for f in os.listdir(config.MC_DIR + "/tmp/" + modpackName) if os.path.isfile(config.MC_DIR + "/instances/" + modpackJsonName + "/" + f)]
        try:
            for file in files:
                if (file.lower().__contains__("readme") or file.lower().__contains__("read me") or file.lower().__contains__("contains") or file.lower().__contains__("included")) and file.lower().endswith(".txt"):
                    if sys.platform.startswith('darwin'):
                        subprocess.call(('open', config.MC_DIR + "/instances/" + modpackJsonName + "/" + file))
                    elif os.name == 'nt':
                        os.startfile(config.MC_DIR + "/instances/" + modpackJsonName + "/" + file)
                    elif os.name == 'posix':
                        subprocess.call(('xdg-open', config.MC_DIR + "/instances/" + modpackJsonName + "/" + file))
        except Exception as e:
            print("There was a problem opening readmes.")
            print(e)
        remove_tree(config.MC_DIR + "/tmp/" + modpackName)
    except Exception as e:
        print("Modpack install failed. Try installing again.")
        print(e)


def rmModpack(modpackName, widget, parent):
    confirm = QMessageBox.question(parent, "Are you sure?", "Are you sure?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if confirm == QMessageBox.Yes:
        remove_tree(config.MC_DIR + "/instances/" + modpackName)
        widget.deleteLater()
