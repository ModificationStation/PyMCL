import config
import utils
import os
import sys
import requests
import json
import traceback
import shutil
import distutils
import configparser

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QCheckBox, QApplication


class exportWindow(QWidget):
    currentInstance = ""
    currentInstanceVersion = None
    doSoundRemoval = False
    makePyMCLModpack = False
    doClassRemoval = False
    doLWJGLRemoval = False

    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Modpack Exporter"
        config.ICON = utils.loadImage("favicon.ico", "")
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - 450
        self.top = screen_resolution.height() / 2 - 220
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 450, 220)
        self.setFixedSize(self.size())
        self.createButtons()
        self.createCheckBoxes()
        self.show()

    def createButtons(self):
        self.instanceSelect = QComboBox(self)
        item = 0
        self.instanceSelect.clear()
        for instance in os.listdir(config.MC_DIR + "/instances"):  # Instances will be verified before being listed in the future,
            self.instanceSelect.addItem(instance)
        if os.path.exists(config.MC_DIR + "/instances/" + self.currentInstance):
            item = self.instanceSelect.findText(self.currentInstance)
        self.instanceSelect.setCurrentIndex(item)
        self.currentInstance = self.instanceSelect.currentText()
        self.instanceSelect.activated[str].connect(self.setInstance)
        self.instanceSelect.move(5, 5)

        self.createModpackButton = QPushButton(self)
        self.createModpackButton.clicked.connect(self.createModpack)
        self.createModpackButton.setText("Export Modpack")
        self.createModpackButton.move(5, 175)
        self.createLabel = QLabel(self, text="Program will stop responding for a few seconds. Keep an eye on the console.")
        self.createLabel.move(5, 200)

    def createCheckBoxes(self):
        self.doSoundRemovalCheckbox = QCheckBox(self)
        self.doSoundRemovalCheckbox.move(5, 30)
        self.doSoundRemovalCheckbox.clicked.connect(self.updateSoundRemoval)
        self.label1 = QLabel(self, text="Do vanilla resources removal. Keeps any changed resource files.")
        self.label1.move(30, 30)

        self.doClassRemovalCheckbox = QCheckBox(self)
        self.doClassRemovalCheckbox.move(5, 50)
        self.doClassRemovalCheckbox.clicked.connect(self.updateClassRemoval)
        self.label2 = QLabel(self, text="Do vanilla class removal. Keeps any changed class files.")
        self.label2.move(30, 50)

        self.doLWJGLRemovalCheckbox = QCheckBox(self)
        self.doLWJGLRemovalCheckbox.move(5, 70)
        self.doLWJGLRemovalCheckbox.clicked.connect(self.updateLWJGLRemoval)
        self.label3 = QLabel(self, text="Do LWJGL removal.")
        self.label3.move(30, 70)

        self.makePyMCLModpackCheckbox = QCheckBox(self)
        self.makePyMCLModpackCheckbox.move(5, 100)
        self.makePyMCLModpackCheckbox.clicked.connect(self.updateMakePyMCLModpack)
        self.label4 = QLabel(self, text="Make PyMCL modpack.")
        self.label4.move(30, 100)

    def setInstance(self, instance):
        self.currentInstance = instance
        try:
            with open(config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft/modpack.json") as file:
                self.currentInstanceVersion = json.loads(file.read())["mcver"]
        except:
            self.currentInstanceVersion = None

    def updateSoundRemoval(self):
        self.doSoundRemoval = self.doSoundRemovalCheckbox.isChecked()
        if self.doLWJGLRemoval and self.doSoundRemoval and self.doClassRemoval:
            self.makePyMCLModpack = True
            self.makePyMCLModpackCheckbox.setChecked(True)
        else:
            self.makePyMCLModpack = False
            self.makePyMCLModpackCheckbox.setChecked(False)

    def updateClassRemoval(self):
        self.doClassRemoval = self.doClassRemovalCheckbox.isChecked()
        if self.doLWJGLRemoval and self.doSoundRemoval and self.doClassRemoval:
            self.makePyMCLModpack = True
            self.makePyMCLModpackCheckbox.setChecked(True)
        else:
            self.makePyMCLModpack = False
            self.makePyMCLModpackCheckbox.setChecked(False)

    def updateLWJGLRemoval(self):
        self.doLWJGLRemoval = self.doLWJGLRemovalCheckbox.isChecked()
        if self.doLWJGLRemoval and self.doSoundRemoval and self.doClassRemoval:
            self.makePyMCLModpack = True
            self.makePyMCLModpackCheckbox.setChecked(True)
        else:
            self.makePyMCLModpack = False
            self.makePyMCLModpackCheckbox.setChecked(False)


    def updateMakePyMCLModpack(self):
        isChecked = self.makePyMCLModpackCheckbox.isChecked()
        self.makePyMCLModpack = isChecked
        self.doLWJGLRemovalCheckbox.setChecked(isChecked)
        self.doLWJGLRemoval = isChecked
        self.doClassRemovalCheckbox.setChecked(isChecked)
        self.doClassRemoval = isChecked
        self.doSoundRemovalCheckbox.setChecked(isChecked)
        self.doSoundRemoval = isChecked

    def createModpack(self):
        utils.logger.info("Copying instance to ~/tmp")
        shutil.copytree(config.MC_DIR + "/instances/" + self.currentInstance, config.MC_DIR + "/tmp/" + self.currentInstance)
        utils.logger.info("Copied.")
        binpath = config.MC_DIR + "/tmp/" + self.currentInstance + "/.minecraft/bin/"
        mcpath = config.MC_DIR + "/tmp/" + self.currentInstance + "/.minecraft/"

        if self.doSoundRemoval or self.makePyMCLModpack:
            utils.logger.info("Getting sound MD5")
            try:
                soundsMD5 = self.getSoundMD5()
                utils.logger.info("MD5 retrieved.\nCulling vanilla resources")
                self.cull("resources", soundsMD5)
                utils.logger.info("Vanilla resources removed.")
            except:
                utils.print_exc()
                utils.logger.info("An error occurred when trying to remove vanilla resources.")

        if self.doClassRemoval or self.makePyMCLModpack:
            utils.logger.info("Extracting minecraft.jar")
            try:
                shutil.unpack_archive(binpath + "minecraft.jar", binpath + "minecraft", "zip")
                utils.logger.info("Extracted.\nGetting class md5")
                classMD5 = self.getClassMD5()
                utils.logger.info("MD5 Retrieved.\nCulling vanilla classes")
                self.cull("bin/minecraft", classMD5)
                utils.logger.info("Vanilla classes removed.\nRepacking jar")
                shutil.make_archive(binpath + "minecraft", "zip", binpath + "minecraft")
                try:
                    os.unlink(binpath + "minecraft.jar")
                except:
                    utils.print_exc()
                os.rename(binpath + "minecraft.zip", binpath + "minecraft.jar")
                shutil.rmtree(binpath + "minecraft")
            except:
                utils.print_exc()
                utils.logger.info("An error occurred when trying to remove vanilla resources.")

        if self.doLWJGLRemoval or self.makePyMCLModpack:
            utils.logger.info("Removing LWJGL files.")
            try:
                os.unlink(binpath + "lwjgl.jar")
            except:
                pass
            try:
                os.unlink(binpath + "lwjgl_util.jar")
            except:
                pass
            try:
                os.unlink(binpath + "jinput.jar")
            except:
                pass
            try:
                os.unlink(binpath + "license.txt")
            except:
                pass
            try:
                shutil.rmtree(binpath + "natives")
            except:
                pass
            utils.logger.info("LWJGL files removed, if any existed.")
        utils.logger.info("Creating modpack.")
        shutil.make_archive(config.MC_DIR + "/tmp/" + self.currentInstance, "zip", config.MC_DIR + "/tmp/" + self.currentInstance)
        utils.logger.info("Modpack created.\nMoving to export folder.")

        utils.areYouThere(config.MC_DIR + "/modpackzips/export/")
        if os.path.exists(config.MC_DIR + "/modpackzips/export/" + self.currentInstance + ".zip"):
            os.unlink(config.MC_DIR + "/modpackzips/export/" + self.currentInstance + ".zip")

        shutil.move(config.MC_DIR + "/tmp/" + self.currentInstance + ".zip", config.MC_DIR + "/modpackzips/export")

        utils.logger.info("Modpack created.\nBe sure to make a modpack.json file for the modpack!")


    # Screw XML. It's terrible. I chose to use it because I only had to add a single 10 character line to my minecraft resources php file. Fight me.
    @staticmethod
    def getSoundMD5():
        md5Array = {}
        with requests.get("http://resourceproxy.pymcl.net/MinecraftResources") as response:
            trip = False
            for string in response.text.split("<Key>"):
                if trip:
                    md5Array[string.split("</Key>")[0]] = string.split("<MD5>")[1].split("</MD5>")[0]
                else:
                    trip = True

        return md5Array

    def getClassMD5(self):

        utils.logger.info("https://files.pymcl.net/client/" + self.currentInstanceVersion + "/classmd5.json")
        try:
            with requests.get("https://files.pymcl.net/client/" + self.currentInstanceVersion + "/classmd5.json") as response:
                classMD5 = json.loads(response.content)
        except:
            utils.print_exc()
            classMD5 = None

        return classMD5

    def cull(self, pathininstance, md5List):
        base = (config.MC_DIR + "/tmp/" + self.currentInstance + "/.minecraft/" + pathininstance).replace("\\", "/") + "/"
        utils.logger.info(base)
        for root, dirs, files in os.walk(base):
            root = root.replace("\\", "/") + "/"

            root = root.replace("//", "/")
            for file in files:
                try:
                    if utils.md5(root + file) == md5List[root.replace(base, "") + file]:
                        os.unlink(root + file)
                except KeyError:
                    pass


    def closeEvent(self, QCloseEvent):
        shutil.rmtree(config.MC_DIR + "/tmp")


try:
    shutil.rmtree(config.MC_DIR + "/tmp")
except:
    pass
utils.areYouThere(config.MC_DIR + "/tmp")

app = QApplication([])
exportWin = exportWindow()

sys.exit(app.exec_())
