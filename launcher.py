import config
import json
import math
import os
import requests
import subprocess
import sys
import threading

from PyQt5.QtCore import pyqtSlot, Qt, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return base_path + "/" + relative_path


def load_image(relative_path):
    try:
        if not os.path.exists(config.MC_DIR + "/theme/" + relative_path):
            print("No Theme")
            raise IOError
        img = QPixmap(config.MC_DIR + "/theme/" + relative_path)
    except IOError:
        img = QPixmap(resource_path(relative_path))

    return img


def saveSettings():
    file = open(config.MC_DIR + "/launcher_config.json", "w")
    file.write(json.dumps(launcherConfig, indent=4, sort_keys=True))
    file.close()


class mainWindow(QWidget):
    guiElements = []
    dirt = []
    guiMove = []

    def __init__(self):
        super().__init__()
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - (854 / 2)
        self.top = screen_resolution.height() / 2 - (480 / 2)
        self.dirtImage = QPixmap(config.BOTTOM_BACKGROUND)
        self.logoImage = QPixmap(config.LOGO)
        self.loadSettings()
        self.initUI()

    def loadSettings(self):
        if not os.path.exists(config.MC_DIR):
            # noinspection PyCallByClass,PyTypeChecker
            self.error("Missing Minecraft directory. Is minecraft installed?")
            os.makedirs(config.MC_DIR + "/.minecraft")
        global launcherConfig
        if not os.path.exists(config.MC_DIR + "/launcher_config.json"):
            file = open(config.MC_DIR + "/launcher_config.json", "w")
            file.write(config.DEFAULT_CONFIG)
            file.close()
        file = open(config.MC_DIR + "/launcher_config.json", "r")
        launcherConfig = json.loads(file.read())
        file.close()

    def initUI(self):
        global threadingEvent, update
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 854, 480)
        self.colorBackground()
        self.createButtons()
        self.createLogin()
        self.createLogo()
        self.createTheInternet()
        self.show()
        self.checkAlive(threadingEvent)
        r = requests.get(config.TEST_URL)
        if r.status_code != 204:
            self.error("Unable to connect to the internet. Updates are disabled.")
            update = False

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
        self.launch()
        self.loginButton.setEnabled(False)
        self.loginBox.setEnabled(False)
        self.optionButton.setEnabled(False)

    @pyqtSlot()
    def optionsMenu(self):
        self.optionWindow = optionWindow(self).exec_()

    def colorBackground(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkGray)
        self.setPalette(p)

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
        self.passBox.setText("Coming soon!")
        self.passBox.setEnabled(False)

    def createLogo(self):
        self.logo = QLabel(self)
        self.logo.resize(256, 49)
        self.logo.setPixmap(self.logoImage.scaled(self.logo.size(), Qt.KeepAspectRatio))

    def createTheInternet(self):
        self.theInternet = QWebEngineView(self)
        self.theInternet.load(QUrl("https://mcupdate.tumblr.com"))
        self.theInternet.show()

    def createImages(self):
        for index in range(len(self.dirt)):
            for indexy in range(len(self.dirt[index])):
                self.dirt[index][indexy].deleteLater()

        self.dirt = []

        for index in range(math.ceil(self.size().width() / 64)):
            self.dirt.append([])
            self.dirt[index].append(QLabel(self))
            self.dirt[index].append(QLabel(self))

        for index in range(math.ceil(self.size().width() / 64)):
            for indexy in range(len(self.dirt[0])):
                self.dirt[index][indexy].show()
                self.dirt[index][indexy].resize(64, 64)
                self.dirt[index][indexy].setPixmap(self.dirtImage)
                self.dirt[index][indexy].move(64 * index, self.size().height() - 100 + (indexy * 64))

        self.logo.raise_()

    # Game ---------------------------------------------------------------------------------------

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
            except:
                pass
            running = False
        if not threadingEvent.is_set():
            checkAliveTimer = threading.Timer(1, self.checkAlive, [threadingEvent])
            checkAliveTimer.start()

    def launch(self):
        global prc, launcherConfig
        try:
            prc.kill()
        except:
            pass
        try:
            if self.loginBox.text() == "":
                raise TypeError
            elif not self.loginBox.text().isalnum():
                raise TypeError
            prc = subprocess.Popen(
                'java {} -Xms{} -Xmx{} -cp "{}\\bin\\minecraft.jar;{}\\bin\\jinput.jar;{}\\bin\\lwjgl.jar;{}\\bin\\lwjgl_util.jar" -Djava.library.path="{}\\bin\\natives" net.minecraft.client.Minecraft {}'.format(
                    launcherConfig["javaargs"], launcherConfig["minram"], launcherConfig["maxram"], config.MC_DIR,
                    config.MC_DIR, config.MC_DIR, config.MC_DIR, config.MC_DIR, launcherConfig["lastusedname"]))
            launcherConfig["lastusedname"] = self.loginBox.text()
            saveSettings()
        except:
            self.error(
                "Minecraft is unable to start. Make sure you have java and minecraft installed and an alphanumeric username set.")

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
        checkAliveTimer.cancel()


class optionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        mainWindow.loadSettings(mainWindow)
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Options"
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - (480 / 2)
        self.top = screen_resolution.height() / 2 - (240 / 2)
        self.logoImage = QPixmap(config.LOGO)
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
        saveSettings()


update = True
prc = ""
running = False
threadingEvent = threading.Event()

app = QApplication(sys.argv)
config.ICON = load_image(config.ICON)
config.LOGO = load_image(config.LOGO)
config.BOTTOM_BACKGROUND = load_image(config.BOTTOM_BACKGROUND)
mainWin = mainWindow()

sys.exit(app.exec_())
