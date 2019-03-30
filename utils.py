import config
import shutil
import zipfile
import os
import io
import urllib
import subprocess
import hashlib
import traceback
import webbrowser
import sys
import requests
import json
import asyncio

from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from distutils.dir_util import copy_tree, remove_tree

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
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
        saveSettings(json.loads(config.DEFAULT_LAUNCHER_CONFIG))
    try:
        with open(config.MC_DIR + "/launcher_config.json", "r") as file:
            launcherConfig = json.loads(file.read())
    except:
        print("Couldn't read launcher config. Renamed to \"instance_config.json.bak\"")
        shutil.move(config.MC_DIR + "/launcher_config.json", config.MC_DIR + "/launcher_config.json.bak")
        saveSettings(config.DEFAULT_INSTANCE_CONFIG)
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
            instanceConfig["minram"]
            instanceConfig["maxram"]
            instanceConfig["javaargs"]
            instanceConfig["proxyskin"]
            instanceConfig["proxysound"]
            instanceConfig["proxycape"]
        except:
            self.error("Couldn't read instance config. Renamed to \"instance_config.json.bak\"")
            shutil.move(config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json", config.MC_DIR + "/instances/" + currentInstance + "/instance_config.json.bak")
            saveInstanceSettings(json.loads(config.DEFAULT_INSTANCE_CONFIG), currentInstance)
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


# Im not even sure this is the way you are meant to do this, but im pretty sure it works. Correct me if im wrong.
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
    data = json.loads(data.content)

    try:
        return True, " --username=" + data["selectedProfile"]["name"] + " --session-id=" + data["accessToken"]
    except KeyError:
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
    installModpack = pyqtSignal(str)
    starting = pyqtSignal()
    updateIStatus = pyqtSignal(str)

    def __init__(self, modpackURL=None):
        super().__init__()
        self.modpackURL = modpackURL

    def run(self):
        self.starting.emit()
        print("getting modpack from url")
        if not self.modpackURL:
            modpackName = "Error"
        else:
            try:
                areYouThere(config.MC_DIR+"/modpackzips/")
                areYouThere(config.MC_DIR+"/tmp/")
                modpackName = urllib.parse.unquote_plus(self.modpackURL.rsplit('/', 1)[-1].split(".")[0])
                if os.path.exists(config.MC_DIR + "/modpackzips/" + modpackName + ".zip"):
                    self.updateIStatus.emit("Using cached file.")
                else:
                    self.updateIStatus.emit("Attempting download...")
                    response = requests.get(self.modpackURL, stream=True)
                    total_length = response.headers.get("content-length")
                    if response.content is None:
                        raise ConnectionError

                    dl = 0
                    total_length = int(total_length)
                    with io.open(config.MC_DIR + "/tmp/" + modpackName + ".zip", 'wb') as fd:
                        oldDone = 0
                        for chunk in response.iter_content(chunk_size=4096):
                            dl += len(chunk)
                            fd.write(chunk)
                            done = int(50 * dl / total_length)
                            if done != oldDone:
                                self.updateIStatus.emit("[%s%s]" % ("=" * done, " " * (50-done)))
                                oldDone = done
                    shutil.move(config.MC_DIR + "/tmp/" + modpackName + ".zip", config.MC_DIR + "/modpackzips/")
            except:
                modpackName = "Error"
        self.installModpack.emit(modpackName)

    def stop(self):
        self.threadactive = False
        self.wait()


# Pretty simple, tries to copy modpack to /modpackzips/, returning error if something went wrong.
class getModpackFS(QThread):
    installModpack = pyqtSignal(str)
    starting = pyqtSignal()
    updateIStatus = pyqtSignal(str)
    updateStatus = pyqtSignal(str)

    def __init__(self, modpackDir=None):
        super().__init__()
        self.modpackDir = modpackDir

    def run(self):
        self.starting.emit()
        if not self.modpackDir:
            modpackName = "Error"
        else:
            self.updateIStatus.emit("Retrieving modpack from path...")
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
                traceback.print_exc()
                modpackName = "Error"
        self.updateStatus.emit("Modpack cached. Starting install.")
        self.updateIStatus.emit("Modpack cached. Starting install.")
        self.installModpack.emit(modpackName)

    def stop(self):
        self.threadactive = False
        self.wait()


class getModpackRepo(QThread):
    result = pyqtSignal(bool, dict)

    def run(self):
        print("Trying")
        try:
            with requests.get("https://modpacks.pymcl.net/api/getmodpacks.php") as response:
                self.result.emit(True, json.loads(response.content))
                print("Worked")
        except:
            self.result.emit(False, {})
            print("Failed")

    def stop(self):
        self.threadactive = False
        self.wait()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def openModpackInBrowser(modpackID=None, url=None):
    if not url:
        url = "https://modpacks.pymcl.net/showmodpack.php?modpack=" + modpackID
    webbrowser.open(url)


# Ugh, i have to comment this? fine.
class installModpack(QThread):
    done = pyqtSignal()
    starting = pyqtSignal()
    updateIStatus = pyqtSignal(str)
    updateStatus = pyqtSignal(str, str)

    def __init__(self, modpackName=None):
        super().__init__()
        self.modpackName = modpackName

    def run(self):
        print("starting")
        self.starting.emit()
        print("Installing modpack")
        try:
            if self.modpackName == "Error" or self.modpackName is None:
                traceback.print_exc()
                raise IOError("Modpack does not exist in directory?")
            if not os.path.exists(config.MC_DIR + "/tmp/" + self.modpackName):
                os.makedirs(config.MC_DIR + "/tmp/" + self.modpackName)

            # Extracts the zip file to the temp dir.
            self.updateIStatus.emit("Extracting modpack...")
            with zipfile.ZipFile(config.MC_DIR + "/modpackzips/" + self.modpackName + ".zip", "r") as zip:
                zip.extractall(config.MC_DIR + "/tmp/" + self.modpackName)

            # Get the modpack's name. if it cant find one, then it uses the name of the zip.
            self.updateIStatus.emit("Installing modpack...")
            try:
                with open(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/modpack.json", "r") as file:
                    modpackJson = json.loads(file.read())
                    modpackJsonName = modpackJson["modpackname"]
                    try:
                        mcVer = modpackJson["mcver"]
                    except:
                        mcVer = None
            except:
                traceback.print_exc()
                self.updateIStatus.emit("No modpack name found. Using zip file name. Get the modpack author to create a \"modpack.json\" file in his/her modpack.")
                modpackJsonName = self.modpackName
                mcVer = None

            if mcVer:
                self.makeModpack(mcVer)

            areYouThere(config.MC_DIR + "/instances/" + modpackJsonName)

            copy_tree(config.MC_DIR + "/tmp/" + self.modpackName, config.MC_DIR + "/instances/" + modpackJsonName)
            self.updateIStatus.emit("Finding Readmes")

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
            except Exception as e:
                traceback.print_exc()
                print("There was a problem opening readmes.")

            # Gotta stay clean!
            self.updateIStatus.emit("Deleting temp files...")
            #remove_tree(config.MC_DIR + "/tmp/" + self.modpackName)
            self.updateStatus.emit("Modpack installed!", "green")

        # And in case the zip didnt exist in the first place.
        except Exception as e:
            self.updateStatus.emit("Modpack install failed. Make sure the URL/filename is correct.", "red")
            traceback.print_exc()
        self.done.emit()

    def makeModpack(self, mcVer):

        self.updateIStatus.emit("Getting versions..")

        with requests.get("https://files.pymcl.net/client/versions.json") as response:
            versionID = json.loads(response.content)[mcVer]

        self.updateIStatus.emit("Downloading minecraft.jar..")

        self.updateIStatus.emit("Attempting version download...")
        response = requests.get("https://launcher.mojang.com/v1/objects/" + versionID + "/client.jar", stream=True)
        total_length = response.headers.get("content-length")
        if response.content is None:
            raise ConnectionError("Something went very wrong.")

        areYouThere(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin")

        self.updateIStatus.emit("Started connection..")

        dl = 0
        total_length = int(total_length)
        with io.open(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/vanillamc.jar", 'wb') as fd:
            oldDone = 0
            for chunk in response.iter_content(chunk_size=4096):
                dl += len(chunk)
                fd.write(chunk)
                done = int(50 * dl / total_length)
                if done != oldDone:
                    self.updateIStatus.emit("[%s%s]" % ("=" * done, " " * (50-done)))
                    oldDone = done

        self.wait(100)

        self.updateIStatus.emit("Downloaded.\nExtracting vanilla jar..")

        shutil.unpack_archive(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/vanillamc.jar", config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft", "zip")

        self.updateIStatus.emit("Extracted.\nExtracting modpack jar and merging jars..")

        try:
            shutil.unpack_archive(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft.jar", config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft", "zip")
        except:
            traceback.print_exc()
            print("No modpack jar found. Making a vanilla instance with contents of modpack zip.")

        self.updateIStatus.emit("Extracted.\nArchiving..")

        shutil.make_archive(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft", "zip", config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft")

        try:
            os.remove(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft.jar")
        except:
            traceback.print_exc()

        os.rename(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft.zip", config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft.jar")

        self.updateIStatus.emit("Archived.\nDownloading LWJGL for " + config.OS + "..")

        response = requests.get("https://files.pymcl.net/client/lwjgl/lwjgl." + config.OS + ".zip", stream=True)
        total_length = response.headers.get("content-length")

        self.updateIStatus.emit("Started connection..")

        dl = 0
        total_length = int(total_length)
        with io.open(config.MC_DIR + "/tmp/lwjgl.zip", 'wb') as fd:
            oldDone = 0
            for chunk in response.iter_content(chunk_size=4096):
                dl += len(chunk)
                fd.write(chunk)
                done = int(50 * dl / total_length)
                if done != oldDone:
                    self.updateIStatus.emit("[%s%s]" % ("=" * done, " " * (50-done)))
                    oldDone = done

        self.updateIStatus.emit("Downloaded.\nExtracting LWJGL..")

        shutil.unpack_archive(config.MC_DIR + "/tmp/lwjgl.zip", config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin")

        self.updateIStatus.emit("Extracted.\nCleaning up..")

        shutil.rmtree(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/minecraft")
        os.remove(config.MC_DIR + "/tmp/" + self.modpackName + "/.minecraft/bin/vanillamc.jar")

    def stop(self):
        self.threadactive = False
        self.wait()


# Simply deletes a given instance.
def rmInstance(instanceName, self):
    confirm = QMessageBox.question(self, "Are you sure?", "Are you sure you want to delete " + instanceName + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    self.updateStatus("Deleting instance \"" + instanceName + "\"...")
    if confirm == QMessageBox.Yes:
        remove_tree(config.MC_DIR + "/instances/" + instanceName)
    try:
        self.updateInstanceList()
        self.updateStatus("Instance \"" + instanceName + "\" deleted.")
    except:
        pass


class minecraftProxy(QThread):

    def __init__(self, doSkinFix, doSoundFix, doCapeFix, loop):
        super().__init__()
        self.doSkinFix = doSkinFix
        self.doCapeFix = doCapeFix
        self.doSoundFix = doSoundFix
        self.loop = loop

    def getHeader(self):
        class AddHeader:
            def __init__(self, parent):
                self.parent = parent

            def request(self, flow):
                if flow.request.pretty_host == "s3.amazonaws.com":

                    if self.parent.doSoundFix:
                        if flow.request.path.__contains__("MinecraftResources"):
                            flow.request.host = "resourceproxy.pymcl.net"

                    if self.parent.doSkinFix:
                        if flow.request.path.__contains__("MinecraftSkins"):
                            flow.request.host = "resourceproxy.pymcl.net"
                            flow.request.path = "/skinapi.php?user=" + flow.request.path.split("/")[2].split(".")[0]

                    if self.parent.doCapeFix:
                        if flow.request.path.__contains__("MinecraftCloaks"):
                            flow.request.host = "resourceproxy.pymcl.net"
                            flow.request.path = "/capeapi.php?user=" + flow.request.path.split("/")[2].split(".")[0]

                if flow.request.pretty_host.__contains__("minecraft.net"):
                    if self.parent.doSkinFix:
                        if flow.request.path.__contains__("skin"):
                            flow.request.host = "resourceproxy.pymcl.net"
                            flow.request.path = "/skinapi.php?user=" + flow.request.path.split("/")[2].split(".")[0]

                    if self.parent.doCapeFix:
                        if flow.request.path.__contains__("cloak"):
                            flow.request.host = "resourceproxy.pymcl.net"
                            flow.request.path = "/capeapi.php?user=" + flow.request.path.split("=")[1]

        return AddHeader(self)

    def run(self):
        asyncio.set_event_loop(self.loop)
        myaddon = self.getHeader()
        opts = options.Options(listen_host="0.0.0.0", listen_port=25560)
        pconf = proxy.config.ProxyConfig(opts)
        self.m = DumpMaster(opts)
        self.m.server = proxy.server.ProxyServer(pconf)
        self.m.addons.add(myaddon)

        self.m.run()

    def stop(self):
        self.m.shutdown()


# Deletes given modpack zip. Prompts if attached to a window. Deletes the widget if attached to one.
def rmModpack(zipName, self=None):
    if not self:
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
