import sys
import config
import requests
import shutil
import json
import zipfile
import os
import io
import urllib
import subprocess
import traceback
from distutils.dir_util import copy_tree, remove_tree

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QLabel

# The shit im actually somewhat good at.


# The installer extracts all the images and files to _MEIPASS, so this is how we get them.
def resourcePath(relative_path):
    # Gets the _MEIPASS sys variable. If _MEIPASS doesnt exist, then it just gets from the local directory. (This allows me to test without compiling)
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))  # I ONLY DEAL IN ABSOLUTES
    return base_path + "/" + relative_path


# Mostly a wrapper function, this is what allows for theming.
# Yes, you could put a theme in /instances/ and you would have a theme when there are no instances.
def loadImage(relative_path, instanceName=""):
    if not os.path.exists(config.MC_DIR + "/instances/" + instanceName + "/theme/" + relative_path):
        img = QPixmap(resourcePath(relative_path))
    else:
        img = QPixmap(config.MC_DIR + "/instances/" + instanceName + "/theme/" + relative_path)
    return img


# Same drill with loadImage(), but it only gets the file path.
def getFile(relative_path, instanceName=""):
    if not os.path.exists(config.MC_DIR + "/instances/" + instanceName + "/theme/" + relative_path):
        img = resourcePath(relative_path)
    else:
        img = config.MC_DIR + "/instances/" + instanceName + "/theme/" + relative_path
    return img


# Loads the settings. If the config doesnt exist, then it makes one with the default config from config.py
# If the json is malformed, then it backs it up and remakes it.
def loadSettings(self):
    if not os.path.exists(config.MC_DIR + "/launcher_config.json"):
        saveSettings(config.DEFAULT_LAUNCHER_CONFIG)
    try:
        with open(config.MC_DIR + "/launcher_config.json", "r") as file:
            launcherConfig = json.loads(file.read())
    except:
        self.error("Couldn't read instance config. Renamed to \"instance_config.json.bak\"")
        shutil.move(config.MC_DIR + "/launcher_config.json", config.MC_DIR + "/launcher_config.bak")
        saveSettings(config.DEFAULT_LAUNCHER_CONFIG)
        with open(config.MC_DIR + "/launcher_config.json", "r") as file:
            launcherConfig = json.loads(file.read())

    return launcherConfig


# Exactly the same as loadsettings, but it gets instance specific config.
def loadInstanceSettings(self, currentInstance):
    if currentInstance != "":
        if not os.path.exists(config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json"):
            saveInstanceSettings(json.loads(config.DEFAULT_INSTANCE_CONFIG), currentInstance)
        try:
            with open(config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json", "r") as file:
                instanceConfig = json.loads(file.read())
        except:
            self.error("Couldn't read instance config. Renamed to \"instance_config.json.bak\"")
            shutil.move(config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json", config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json.bak")
            saveInstanceSettings(config.DEFAULT_INSTANCE_CONFIG, currentInstance)
            with open(config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json", "r") as file:
                instanceConfig = json.loads(file.read())
    else:
        instanceConfig = json.loads(config.DEFAULT_INSTANCE_CONFIG)

    return instanceConfig


# I made these because im lazy.
def saveSettings(conf):
    with open(config.MC_DIR + "/launcher_config.json", "w") as file:
        file.write(json.dumps(conf, indent=4, sort_keys=True))


def saveInstanceSettings(conf, currentInstance):
    if not currentInstance == "":
        with open(config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json", "w") as file:
            file.write(json.dumps(conf, indent=4, sort_keys=True))


# Im not even sure this is the way you are meant to do this, but im pretty sure it works.
# This retrieves the name and session from the provided details.
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
    print(data.content)
    data = json.loads(data.content)

    try:
        return True, data["selectedProfile"]["name"] + " " + data["accessToken"]
    except AttributeError:
        return False, None


# Unused
def checkOnline():
    try:
        requests.get("http://google.com/generate_204")
        return True
    except:
        return False


# Unused
def getModpacks():
    data = requests.get(config.UPDATE_URL)
    return data


# Again, because im lazy. Simply creates a dir if it doesnt exist.
def areYouThere(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Fetches mdpack from url and shoves it into modpackzips. Returns Error if something went wrong.
class getModpackURL(QThread):
    modpackURL = None
    win = None
    installModpack = pyqtSignal(QObject, str)
    starting = pyqtSignal()

    def run(self):
        self.starting.emit()
        if not self.modpackURL or not self.win:
            modpackName = "Error"
        else:
            try:
                if not os.path.exists(config.MC_DIR+"/modpackzips/"):
                    os.makedirs(config.MC_DIR+"/modpackzips/")
                modpackName = urllib.parse.unquote_plus(self.modpackURL.rsplit('/', 1)[-1].split(".")[0])
                if os.path.exists(config.MC_DIR + "/modpackzips/" + modpackName + ".zip"):
                    self.win.updateStatus("Using cached file.")
                else:
                    self.win.updateStatus("Attempting download...")
                    response = requests.get(self.modpackURL, stream=True)
                    with io.open(config.MC_DIR + "/modpackzips/" + modpackName + ".zip", 'wb') as fd:
                        for chunk in response.iter_content(chunk_size=4096):
                            fd.write(chunk)
            except:
                modpackName = "Error"
        self.installModpack.emit(self.win, modpackName)


# Pretty simple, tries to copy modpack to /modpackzips/, returning error if something went wrong.
class getModpackFS(QThread):
    modpackDir = None
    win = None
    installModpack = pyqtSignal(QObject, str)
    starting = pyqtSignal()

    def run(self):
        self.starting.emit()
        if not self.modpackDir or not self.win:
            modpackName = "Error"
        else:
            self.win.updateStatus("Retrieving modpack from path...")
            if not os.path.exists(config.MC_DIR+"/modpackzips/"):
                os.makedirs(config.MC_DIR+"/modpackzips/")
            try:
                modpackName = os.path.splitext(os.path.basename(self.modpackDir))[0]
            except:
                modpackName = "Error"
            if os.path.exists(config.MC_DIR + "/modpackzips/" + modpackName + ".zip"):
                os.remove(config.MC_DIR + "/modpackzips/" + modpackName + ".zip")
            try:
                shutil.copy(self.modpackDir, config.MC_DIR + "/modpackzips/"+modpackName + ".zip")
            except:
                modpackName = "Error"
        self.installModpack.emit(self.win, modpackName)


# Ugh, i have to comment this? fine.
class installModpack(QThread):
    modpackName = None
    win = None
    done = pyqtSignal()
    starting = pyqtSignal()

    def run(self):
        self.starting.emit()
        try:
            if self.modpackName == "Error":
                raise IOError("Modpack does not exist in directory?")
            if not os.path.exists(config.MC_DIR + "/tmp/" + self.modpackName):
                os.makedirs(config.MC_DIR + "/tmp/" + self.modpackName)

            # Extracts the zip file to the temp dir.
                self.win.updateStatus("Extracting modpack...")
            with zipfile.ZipFile(config.MC_DIR + "/modpackzips/" + self.modpackName + ".zip", "r") as zip:
                zip.extractall(config.MC_DIR + "/tmp/" + self.modpackName)

            # Get the modpack's name. if it cant find one, then it uses the name of the zip.
            self.win.updateStatus("Installing modpack...")
            try:
                with open(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/modpack.json", "r") as file:
                    modpackJson = json.loads(file.read())
                    modpackJsonName = modpackJson["modpackname"]
            except:
                print("No modpack name found. Using zip file name. Get the modpack author to create a \"modpack.json\" file in his/her modpack.")
                modpackJsonName = self.modpackName

            areYouThere(config.MC_DIR + "/instances/" + modpackJsonName)

            copy_tree(config.MC_DIR + "/tmp/" + self.modpackName, config.MC_DIR + "/instances/" + modpackJsonName)
            self.win.updateStatus("Finding Readmes")

            # Finds all files that start with readme, read me, contains, included, mod list, modlist and credits.
            files = [f for f in os.listdir(config.MC_DIR + "/instances/" + modpackJsonName) if os.path.isfile(config.MC_DIR + "/instances/" + modpackJsonName + "/" + f)]
            try:
                for file in files:
                    if (file.lower().__contains__("readme") or file.lower().__contains__("read me") or file.lower().__contains__("contains") or
                        file.lower().__contains__("included") or file.lower().__contains__("mod list") or file.lower().__contains__("modlist") or
                        file.lower().__contains__("credits")) and file.lower().endswith(".txt"):

                        # Opens the readme with the user default program.
                        if sys.platform.startswith('darwin'):
                            subprocess.call(('open', config.MC_DIR + "/instances/" + modpackJsonName + "/" + file))
                        elif os.name == 'nt':
                            os.startfile(config.MC_DIR + "/instances/" + modpackJsonName + "/" + file)
                        elif os.name == 'posix':
                            subprocess.call(('xdg-open', config.MC_DIR + "/instances/" + modpackJsonName + "/" + file))

            # In case shit went wrong.
            except:
                print("There was a problem opening readmes.")

            # Gotta stay clean!
            self.win.updateStatus("Deleting temp files...")
            remove_tree(config.MC_DIR + "/tmp/" + self.modpackName)
            self.win.updateStatus("Modpack installed!")

        # And in case the zip didnt exist in the first place.
        except:
            self.win.updateStatus("Modpack install failed. Make sure the URL/filename is correct.", color="red")
        self.done.emit()


class status(QLabel):
    changed = pyqtSignal()

    def setLabelText(self, p_str):
        self.setText(p_str)
        self.changed.emit()


# Simply deletes a given instance.
def rmInstance(instanceName, widget, self):
    confirm = QMessageBox.question(self, "Are you sure?", "Are you sure you want to delete " + instanceName + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    self.updateStatus("Deleting instance \"" + instanceName + "\"...")
    if confirm == QMessageBox.Yes:
        remove_tree(config.MC_DIR + "/instances/" + instanceName)
    try:
        self.updateInstanceList()
        self.updateStatus("Instance \"" + instanceName + "\" deleted.")
    except:
        pass


# Deletes given modpack zip. Prompts if attached to a window. Deletes the widget if attached to one.
def rmModpack(zipName, widget="", self=""):
    if isinstance(self, str):
        confirm = QMessageBox.Yes
    else:
        confirm = QMessageBox.question(self, "Are you sure?", "Are you sure you want to delete " + zipName + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if confirm == QMessageBox.Yes:
        self.updateStatus("Deleting modpack \"" + zipName + "\"...")
        os.remove(config.MC_DIR + "/modpackzips/" + zipName)
    try:
        self.updateInstanceList()
        self.updateStatus("Modpack \"" + zipName + "\" deleted.")
    except:
        pass
