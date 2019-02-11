import config
import utils
from json import loads, dumps
from math import ceil
from os.path import abspath, exists
from os import makedirs, listdir, startfile, chdir, environ
from requests import get as reqGet
import subprocess
import sys
import threading
import shutil
import platform
import traceback
import shlex

from PyQt5.QtCore import pyqtSlot, Qt, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QTabWidget, QComboBox, QScrollArea, QVBoxLayout


class mainWindow(QWidget):
    guiElements = []
    dirt = []
    guiMove = []
    instanceSelect = ""

    def __init__(self):
        super().__init__()
        utils.areYouThere(config.MC_DIR+"/instances")
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER
        config.ICON = utils.loadImage("favicon.ico", currentInstance)
        self.setWindowIcon(QIcon(config.ICON))
        config.LOGO = utils.loadImage("logo.png", currentInstance)
        config.BACKGROUND = utils.loadImage("background.png", currentInstance)
        self.left = screen_resolution.width() / 2 - (854 / 2)
        self.top = screen_resolution.height() / 2 - (480 / 2)
        global launcherConfig
        launcherConfig = utils.loadSettings()
        self.initUI()

    def initUI(self):
        global threadingEvent, update
        update = utils.checkOnline()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 854, 480)
        self.colorBackground()
        self.createButtons()
        self.createLogin()
        self.createDropdowns()
        self.createLogo()
        self.createTheInternet()
        self.show()
        self.checkAlive(threadingEvent)

    @pyqtSlot()
    def resizeEvent(self, event):
        for index in range(len(self.guiElements)):
            self.guiElements[index].move(self.size().width() + self.guiMove[index][0],
                                         self.size().height() + self.guiMove[index][1])
        self.createImages()
        for index in range(len(self.guiElements)):
            self.guiElements[index].raise_()
        self.logo.move(32, self.size().height() - (49 + 32))
        self.theInternet.resize(self.size().width(), self.size().height() - 100)

    @pyqtSlot()
    def login(self):
        global username
        if self.passBox.text() != "":
            username = utils.login(self.loginBox.text(), self.passBox.text())
            if isinstance(username, str):
                self.launch()
            else:
                self.error("Invalid credidentials.")
        else:
            username = self.loginBox.text()
            self.launch()

        self.loginButton.setEnabled(False)
        self.loginBox.setEnabled(False)
        self.passBox.setEnabled(False)
        self.optionButton.setEnabled(False)

    @pyqtSlot()
    def optionsMenu(self):
        self.optionWindow = optionWindow(self).exec_()

    @pyqtSlot()
    def instanceMenu(self):
        self.instanceWindow = instanceWindow(self).exec_()

    def colorBackground(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkGray)
        self.setPalette(p)

    def createDropdowns(self):
        if isinstance(self.instanceSelect, str):
            self.instanceSelect = QComboBox(self)
            self.guiMove.append([-255, -(9 + 22)])
            self.instanceSelect.resize(166, 22)
            self.guiElements.append(self.instanceSelect)
            self.instanceSelect.activated[str].connect(self.setInstance)

            for instance in listdir(config.MC_DIR + "/instances"):
                self.instanceSelect.addItem(instance)
        else:
            self.instanceSelect.clear()
            for instance in listdir(config.MC_DIR + "/instances"):
                self.instanceSelect.addItem(instance)
            item = self.instanceSelect.findText(currentInstance)
            self.instanceSelect.setCurrentIndex(item)

    def createButtons(self):
        self.loginButton = QPushButton("Login", self)
        self.guiMove.append([-(11 + 70), -(35 + 22)])
        self.loginButton.resize(70, 22)
        self.loginButton.clicked.connect(self.login)
        self.guiElements.append(self.loginButton)

        self.optionButton = QPushButton("Options", self)
        self.guiMove.append([-(11 + 70), -(35 + 22 + 4 + 21)])
        self.optionButton.resize(70, 22)
        self.optionButton.clicked.connect(self.optionsMenu)
        self.guiElements.append(self.optionButton)

        self.modpackManageButton = QPushButton("Instances", self)
        self.guiMove.append([-(11 + 70), -(10 + 22)])
        self.modpackManageButton.resize(70, 22)
        self.modpackManageButton.clicked.connect(self.instanceMenu)
        self.guiElements.append(self.modpackManageButton)

    def createLogin(self):
        global launcherConfig
        self.loginBox = QLineEdit(self, text=launcherConfig["lastusedname"])
        self.guiMove.append([-255, -(35 + 22 + 4 + 22)])
        self.loginBox.resize(166, 22)
        self.guiElements.append(self.loginBox)

        self.passBox = QLineEdit(self)
        self.guiMove.append([-255, -(35 + 22)])
        self.passBox.resize(166, 22)
        self.guiElements.append(self.passBox)
        self.passBox.setEchoMode(QLineEdit.Password)

    def createLogo(self):
        self.logo = QLabel(self)
        self.logo.resize(256, 49)
        self.logo.setPixmap(config.LOGO.scaled(self.logo.size(), Qt.KeepAspectRatio))

    def createTheInternet(self):
        self.theInternet = QLabel(self)
        response = reqGet("https://mcupdate.tumblr.com")
        self.theInternet.setText(str(response.content))
        self.theInternet.setTextFormat(Qt.RichText)
        self.theInternet.show()

    def createImages(self):
        for index in range(len(self.dirt)):
            for indexy in range(len(self.dirt[index])):
                self.dirt[index][indexy].deleteLater()

        self.dirt = []

        for index in range(ceil(self.size().width() / 64)):
            self.dirt.append([])
            self.dirt[index].append(QLabel(self))
            self.dirt[index].append(QLabel(self))

        for index in range(ceil(self.size().width() / 64)):
            for indexy in range(len(self.dirt[0])):
                self.dirt[index][indexy].show()
                self.dirt[index][indexy].resize(64, 64)
                self.dirt[index][indexy].setPixmap(config.BACKGROUND.scaled(self.dirt[0][0].size(), Qt.KeepAspectRatio))
                self.dirt[index][indexy].move(64 * index, self.size().height() - 100 + (indexy * 64))

        self.logo.raise_()

    # Game ---------------------------------------------------------------------------------------

    def setInstance(self, text):
        global currentInstance
        currentInstance = text
        config.ICON = utils.loadImage("favicon.ico", currentInstance)
        config.LOGO = utils.loadImage("logo.png", currentInstance)
        config.BACKGROUND = utils.loadImage("background.png", currentInstance)
        self.setWindowIcon(QIcon(config.ICON))
        self.createImages()
        self.logo.setPixmap(config.LOGO.scaled(self.logo.size(), Qt.KeepAspectRatio))
        for index in range(len(self.guiElements)):
            self.guiElements[index].raise_()
        self.logo.raise_()

    def checkAlive(self, threadingEvent):
        global prc, checkAliveTimer, running
        try:
            poll = prc.poll()
            if poll is None:
                running = True
            else:
                raise AttributeError
        except AttributeError:
            try:
                self.loginButton.setEnabled(True)
                self.loginBox.setEnabled(True)
                self.optionButton.setEnabled(True)
                self.passBox.setEnabled(True)
            except:
                pass
            running = False
        if not threadingEvent.is_set():
            checkAliveTimer = threading.Timer(1, self.checkAlive, [threadingEvent])
            checkAliveTimer.start()

    def launch(self):
        global prc, launcherConfig, username, currentInstance
        try:
            prc.kill()
        except:
            pass
        try:
            if self.loginBox.text() == "":
                raise TypeError
            elif not username.isalnum():
                raise TypeError
            # This better damn well work.
            print(platform.platform())
            if platform.platform().startswith("Windows"):
                environ["APPDATA"] = config.MC_DIR + "/instances/" + currentInstance
                prc = subprocess.Popen("java " + launcherConfig["javaargs"] + " -Xms" + launcherConfig["minram"] + " -Xmx" + launcherConfig["maxram"] + " -cp \"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/minecraft.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/jinput.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/lwjgl.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/lwjgl_util.jar\" " + "-Djava.library.path=\"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/natives\" net.minecraft.client.Minecraft " + self.loginBox.text(), env=dict(environ, APPDATA=config.MC_DIR + "/instances/" + currentInstance))
            elif platform.platform().startswith("Darwin"):
                prc = subprocess.Popen("java " + launcherConfig["javaargs"] + " -Xms" + launcherConfig["minram"] + " -Xmx" + launcherConfig["maxram"] + " -cp \"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/minecraft.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/jinput.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/lwjgl.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/lwjgl_util.jar\" " + "-Djava.library.path=\"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/natives\" net.minecraft.client.Minecraft " + self.loginBox.text(), env=dict(environ, HOME=config.MC_DIR + "/instances/" + currentInstance))
            else:
                prc = subprocess.Popen("java " + launcherConfig["javaargs"] + " -Xms" + launcherConfig["minram"] + " -Xmx" + launcherConfig["maxram"] + " -cp \"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/minecraft.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/jinput.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/lwjgl.jar;" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/lwjgl_util.jar\" " + "-Duser.home=\"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "\" -Dminecraft.applet.targetDirectory=\"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "\" -Djava.library.path=\"" + config.MC_DIR + "/instances/" + currentInstance + "/.minecraft" + "/bin/natives\" net.minecraft.client.Minecraft " + self.loginBox.text())
            launcherConfig["lastusedname"] = self.loginBox.text()
            utils.saveSettings(launcherConfig)
        except Exception as e:
            self.error("Minecraft is unable to start. Make sure you have java and minecraft installed and an alphanumeric username set.")
            traceback.print_exc()

    def error(self, err):
        # noinspection PyCallByClass
        QMessageBox.warning(self, "Warning", err, QMessageBox.Ok, QMessageBox.Ok)

    @staticmethod
    def forceQuit():
        global prc
        try:
            prc.kill()
            prc = ""
        except:
            pass

    def closeEvent(self, event):
        global checkAliveTimer
        if exists(config.MC_DIR+"/tmp"):
            shutil.rmtree(config.MC_DIR+"/tmp")
        checkAliveTimer.cancel()


class optionWindow(QDialog):
    def __init__(self, parent=None):
        global launcherConfig
        super().__init__(parent)
        launcherConfig = utils.loadSettings()
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Options"
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - (480 / 2)
        self.top = screen_resolution.height() / 2 - (240 / 2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 480, 240)
        self.setFixedSize(self.size())
        self.createLabels()
        self.createSettingInputs()

    def createSettingInputs(self):
        global launcherConfig
        self.javaArgs = QLineEdit(self, text=launcherConfig["javaargs"])
        self.javaArgs.resize(310, 24)
        self.javaArgs.move(150, 20)

        self.maxRamAllocation = QLineEdit(self, text=launcherConfig["maxram"])
        self.maxRamAllocation.resize(100, 24)
        self.maxRamAllocation.move(150 + 55, 20 + 4 + 24)

        self.minRamAllocation = QLineEdit(self, text=launcherConfig["minram"])
        self.minRamAllocation.resize(100, 24)
        self.minRamAllocation.move(150 + 50 + 60 + 100, 20 + 4 + 24)

    def createLabels(self):
        self.javaArgsLabel = QLabel(self, text="Java arguments:")
        self.javaArgsLabel.resize(100, 20)
        self.javaArgsLabel.move(20, 22)

        self.ramAllocationLabel = QLabel(self, text="RAM Allocation:")
        self.ramAllocationLabel.resize(100, 20)
        self.ramAllocationLabel.move(20, 22 + 6 + 22)

        self.maxRamAllocationLabel = QLabel(self, text="Maximum:")
        self.maxRamAllocationLabel.move(20 + 100 + 30, 22 + 6 + 22)
        self.maxRamAllocationLabel.resize(100, 20)

        self.minRamAllocationLabel = QLabel(self, text="Minimum:")
        self.minRamAllocationLabel.move(20 + 100 + 150 + 40, 22 + 6 + 22)
        self.minRamAllocationLabel.resize(100, 20)

    def closeEvent(self, event, *args, **kwargs):
        global launcherConfig
        launcherConfig["javaargs"] = self.javaArgs.text()
        launcherConfig["minram"] = self.minRamAllocation.text()
        launcherConfig["maxram"] = self.maxRamAllocation.text()
        utils.saveSettings(launcherConfig)


class instanceWindow(QDialog):
    widgets = []

    def __init__(self, parent=None):
        super().__init__(parent)
        launcherConfig = utils.loadSettings()
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Instance Manager"
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - (480 / 2)
        self.top = screen_resolution.height() / 2 - (240 / 2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 480, 240)
        self.setFixedSize(self.size())
        self.listInstances()
        self.createButtons()
        self.createInput()

    def listInstances(self):
        for widget in self.widgets:
            try:
                widget.deleteLater()
            except:pass
        self.widgets=[]
        box = QVBoxLayout(self)
        self.setLayout(box)
        scroll = QScrollArea(self)
        box.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        for instance in listdir(config.MC_DIR+"/instances"):
            widget = QPushButton(self, text="Delete " + instance + ".")
            widget.clicked.connect(lambda: utils.rmModpack(instance, widget, self))
            scrollLayout.addWidget(widget)
            self.widgets.append(widget)
        scroll.setWidget(scrollContent)

    def createButtons(self):
        self.openDirButton = QPushButton("Open " + config.NAME + " Install Dir", self)
        self.openDirButton.resize(150, 22)
        self.openDirButton.move(self.width()-155, 5)
        self.openDirButton.clicked.connect(self.openDir)

        self.installModpackButton = QPushButton("Install Local Modpack", self)
        self.installModpackButton.resize(150, 22)
        self.installModpackButton.move(5, 5)
        self.installModpackButton.clicked.connect(self.installModpack)

    def createInput(self):
        self.modpackZipDir = QLineEdit(self)
        self.modpackZipDir.resize(170, 22)
        self.modpackZipDir.move(155, 5)

    def installModpack(self):
        utils.installModpack(utils.getModapackFS(self.modpackZipDir.text()))

    def openDir(self):
        path = config.MC_DIR
        if platform.system() == "Windows":
            startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def closeEvent(self, event, *args, **kwargs):
        global currentInstance, mainWin
        if not exists(config.MC_DIR + "/instances/" + currentInstance):
            try:
                currentInstance = listdir(config.MC_DIR + "/instances")[0]
            except:
                currentInstance = ""

        mainWindow.setInstance(mainWin, currentInstance)
        mainWindow.createDropdowns(mainWin)


try:
    currentInstance = listdir(config.MC_DIR+"/instances")[0]
except:
    currentInstance = ""

username = ""
update = True
prc = ""
running = False


threadingEvent = threading.Event()

app = QApplication(sys.argv)
mainWin = mainWindow()

sys.exit(app.exec_())
