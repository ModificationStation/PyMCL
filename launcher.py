import config
import utils
import math
import os
import os.path
import subprocess
import sys
import threading
import shutil
import platform
import pypresence
import functools
import urllib

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, \
    QComboBox, QScrollArea, QVBoxLayout, QFileDialog, QTabWidget


class mainWindow(QWidget):
    guiElements = []
    dirt = []
    guiMove = []
    instanceSelect = ""
    creds = ""

    # This is used to init the background crap such as update checking and rich presence.
    def __init__(self):
        super().__init__()
        self.loggedIn = False  # Tells the launcher if the user is logged in.
        utils.areYouThere(config.MC_DIR + "/instances")
        screen_resolution = app.desktop().screenGeometry()  # Gets primary monitor resolution.
        self.title = config.NAME + " " + config.VER
        config.ICON = utils.loadImage("favicon.ico", self.currentInstance)
        self.setWindowIcon(QIcon(config.ICON))
        config.LOGO = utils.loadImage("logo.png", self.currentInstance)
        config.BACKGROUND = utils.loadImage("background.png", self.currentInstance)
        config.BLOG_BACKGROUND = utils.getFile("blogbackground.png", self.currentInstance)
        config.BLOG = utils.getFile("blog.html", self.currentInstance)
        self.left = (screen_resolution.width() / 2) - 427
        self.top = (screen_resolution.height() / 2) - 240
        self.launcherConfig = utils.loadSettings(self)
        self.instanceConfig = utils.loadInstanceSettings(self, self.currentInstance)
        try:
            self.pres = pypresence.Presence("548208354196062228")  # Go ahead and use this if you want, provided you are modifying the launcher. Not that I can really stop you.
            self.pres.connect()
            self.pres.update(details="In launcher", large_image="pymcllogo512", state="Selected modpack: " + self.currentInstance)
        except:
            self.pres = None
        self.checkAlive(threadingEvent)
        self.initUI()

    # This sets up all the crap you see.
    def initUI(self):
        global threadingEvent, update
        update = utils.checkOnline()  # Unused. Gonna be used for update checking and the modpack repo then that is made.
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 854, 480)
        self.colorBackground()
        self.createButtons()
        self.createLogin()
        self.createDropdowns()
        self.createLogo()
        self.createTheInternet()
        self.show()

    # This is fired every time you resize the launcher.
    def resizeEvent(self, event):
        # self.guiElements contains all the elements that get moved when the launcher is resized.
        # This goes though said variable and moves all elements to the relative location specified.
        for index in range(len(self.guiElements)):
            self.guiElements[index].move(self.size().width() + self.guiMove[index][0], self.size().height() + self.guiMove[index][1])

        self.createImages()  # Recreates the dirt background. Works well for now.

        # Just moves all widgets above the dirt background because pyqt layers elements accoring to when they were made.
        for index in range(len(self.guiElements)):
            self.guiElements[index].raise_()

        self.logo.move(32, self.size().height() - 81)
        self.logo.raise_()
        self.theInternet.resize(self.size().width(), self.size().height() - 100)

    # Fired when the login button is pressed.
    def login(self):

        # If the password box is filled out, login and get the user's name and session id.
        if self.passBox.text() != "":
            self.loggedIn, self.creds = utils.login(self.loginBox.text(), self.passBox.text())
            if isinstance(self.creds, str):
                self.launch()
            else:
                self.error("Invalid credidentials.")
        else:
            self.creds = self.loginBox.text()
            self.launch()

        self.loginButton.setEnabled(False)
        self.loginBox.setEnabled(False)
        self.passBox.setEnabled(False)
        self.optionButton.setEnabled(False)
        self.instanceSelect.setEnabled(False)
        self.modpackManageButton.setEnabled(False)

    # Simple wrapper function for showing the options menu.
    def optionsMenu(self):
        self.optionWindow = optionWindow(self).exec_()

    # Simple wrapper function for showing the isntance menu.
    def instanceMenu(self):
        self.instanceWindow = instanceWindow(self).exec_()

    # Honestly, I forgot I even done this. Sets the background colour in case the theme uses transparent images so you dont get an ugly white background.
    def colorBackground(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkGray)
        self.setPalette(p)

    # The names of these create functions are self explanatory.
    def createDropdowns(self):
        if isinstance(self.instanceSelect, str):
            self.instanceSelect = QComboBox(self)
            self.guiMove.append([-255, -31])
            self.instanceSelect.resize(166, 22)
            self.guiElements.append(self.instanceSelect)
            self.instanceSelect.activated[str].connect(self.setInstance)

            for instance in os.listdir(config.MC_DIR + "/instances"):
                self.instanceSelect.addItem(instance)
        else:
            self.instanceSelect.clear()
            for instance in os.listdir(config.MC_DIR + "/instances"):  # Instances will be verified before being listed in the future,
                self.instanceSelect.addItem(instance)
            if os.path.exists(config.MC_DIR + "/instances/" + self.currentInstance):
                item = self.instanceSelect.findText(self.currentInstance)
            self.instanceSelect.setCurrentIndex(item)

    def createButtons(self):
        self.loginButton = QPushButton("Login", self)
        self.guiMove.append([-81, -57])
        self.loginButton.resize(70, 22)
        self.loginButton.clicked.connect(self.login)
        self.guiElements.append(self.loginButton)

        self.optionButton = QPushButton("Options", self)
        self.guiMove.append([-81, -82])
        self.optionButton.resize(70, 22)
        self.optionButton.clicked.connect(self.optionsMenu)
        self.guiElements.append(self.optionButton)

        self.modpackManageButton = QPushButton("Instances", self)
        self.guiMove.append([-81, -32])
        self.modpackManageButton.resize(70, 22)
        self.modpackManageButton.clicked.connect(self.instanceMenu)
        self.guiElements.append(self.modpackManageButton)

    def createLogin(self):
        self.loginBox = QLineEdit(self, text=self.launcherConfig["lastusedname"])
        self.guiMove.append([-255, -83])
        self.loginBox.resize(166, 22)
        self.guiElements.append(self.loginBox)

        self.passBox = QLineEdit(self)
        self.guiMove.append([-255, -57])
        self.passBox.resize(166, 22)
        self.guiElements.append(self.passBox)
        self.passBox.setEchoMode(QLineEdit.Password)

    def createLogo(self):
        self.logo = QLabel(self)
        self.logo.resize(256, 49)
        self.logo.setPixmap(config.LOGO.scaled(self.logo.size(), Qt.KeepAspectRatio))

    # Doesnt actually anymore, but I liked the name, so it stays.
    def createTheInternet(self):
        self.theInternet = QTextEdit(self)
        with open(config.BLOG, "r", encoding="utf-8") as file:
            content = file.read()
        self.theInternet.setHtml(content.replace("&background&", urllib.parse.quote(config.BLOG_BACKGROUND.replace("\\", "/"))))
        self.theInternet.show()
        self.theInternet.setReadOnly(True)

    # This one is kinda smart.
    def createImages(self):
        # Deletes all background image elements.
        for index in range(len(self.dirt)):
            for indexy in range(len(self.dirt[index])):
                self.dirt[index][indexy].deleteLater()

        self.dirt = []

        # Creates as many images as needed to cover the screen.
        for index in range(math.ceil(self.size().width() / 64)):
            self.dirt.append([])
            self.dirt[index].append(QLabel(self))
            self.dirt[index].append(QLabel(self))

        # Moves and resizes and rescales all the images to be a grid of 64x64 images. Supports transparency.
        for index in range(math.ceil(self.size().width() / 64)):
            for indexy in range(len(self.dirt[0])):
                self.dirt[index][indexy].show()
                self.dirt[index][indexy].resize(64, 64)
                self.dirt[index][indexy].setPixmap(config.BACKGROUND.scaled(self.dirt[0][0].size(), Qt.KeepAspectRatio))
                self.dirt[index][indexy].move(64 * index, self.size().height() - 100 + (indexy * 64))

    # Sets the instance selected in the instance select.
    def setInstance(self, instance):
        self.currentInstance = instance

        # Loads the theme in the instance (if any)
        config.ICON = utils.loadImage("favicon.ico", self.currentInstance)
        config.LOGO = utils.loadImage("logo.png", self.currentInstance)
        config.BACKGROUND = utils.loadImage("background.png", self.currentInstance)
        config.BLOG_BACKGROUND = utils.getFile("blogbackground.png", self.currentInstance)
        config.BLOG = utils.getFile("blog.html", self.currentInstance)

        # Sets the theme.
        self.setWindowIcon(QIcon(config.ICON))
        self.createImages()
        self.logo.setPixmap(config.LOGO.scaled(self.logo.size(), Qt.KeepAspectRatio))
        with open(config.BLOG, "r", encoding="utf-8") as file:
            content = file.read()
        self.theInternet.setHtml(content.replace("&background&", urllib.parse.quote(config.BLOG_BACKGROUND.replace("\\", "/"))))
        for index in range(len(self.guiElements)):
            self.guiElements[index].raise_()

        # Finishing touches. The logo needs raising because it isnt on the guielements list.
        self.logo.raise_()
        self.instanceConfig = utils.loadInstanceSettings(self, self.currentInstance)
        try:
            self.pres.update(details="In launcher", large_image="pymcllogo512", state="Selected modpack: " + self.currentInstance)
        except:
            pass

    # Checks if the game is running.
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
                # Enables all the buttons so they can be used again.
                self.loginButton.setEnabled(True)
                self.loginBox.setEnabled(True)
                self.optionButton.setEnabled(True)
                self.passBox.setEnabled(True)
                self.instanceSelect.setEnabled(True)
                self.modpackManageButton.setEnabled(True)

                self.pres.update(details="In launcher", large_image="pymcllogo512", state="Selected modpack: " + self.currentInstance)
            except:
                pass
            running = False
        # If this hasnt been run before, then it creates a timer that runs this every second.
        if not threadingEvent.is_set():
            checkAliveTimer = threading.Timer(1, self.checkAlive, [threadingEvent])
            checkAliveTimer.start()

    # Launches the game.
    def launch(self):
        global prc
        try:
            prc.kill()
        except:
            pass
        try:
            # Checks if the user is an idiot.
            if self.loginBox.text() == "":
                raise TypeError("Username not specified!")
            if self.loggedIn:
                pass
            elif not self.loginBox.text().isalnum():
                raise TypeError("Username not alphanumeric!")
            # This better damn well work. Pretty sure this will though.
            print(platform.platform())
            # If windows, then only override appdata. Otherwise override them all. because compatibility, amirite?
            if platform.platform().startswith("Windows"):
                os.environ["APPDATA"] = config.MC_DIR + "/instances/" + self.currentInstance
            else:
                os.environ["APPDATA"] = config.MC_DIR + "/instances/" + self.currentInstance
                os.environ["USER.HOME"] = config.MC_DIR + "/instances/" + self.currentInstance
                os.environ["HOME"] = config.MC_DIR + "/instances/" + self.currentInstance
            # Launch the game. I ONLY DEAL IN ABSOLUTES. (Lies!)
            prc = subprocess.Popen("java " + self.instanceConfig["javaargs"] + " -Xms" + self.instanceConfig["minram"] + " -Xmx" + self.instanceConfig["maxram"] + " -cp \"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft" + "/bin/minecraft.jar;" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft" + "/bin/jinput.jar;" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft" + "/bin/lwjgl.jar;" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft" + "/bin/lwjgl_util.jar\" " + "-Djava.library.path=\"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft" + "/bin/natives\" net.minecraft.client.Minecraft " + self.creds, env=dict(os.environ))

            self.launcherConfig["lastusedname"] = self.loginBox.text()
            utils.saveSettings(self.launcherConfig)
            try:
                self.pres.update(details="Playing", large_image="pymcllogo512", state="Selected modpack: " + self.currentInstance)
            except:
                pass
            self.loggedIn = False
        except Exception as e:
            # Tragic.
            self.error("Minecraft is unable to start. Make sure you have java and minecraft installed and an alphanumeric username set.")
            print("Rejected username: " + self.loginBox.text())
            print(e)

    # Cause we need an error box thingy without too much copypasta.
    def error(self, err):
        QMessageBox.warning(self, "Warning", err, QMessageBox.Ok, QMessageBox.Ok)

    # Its there, but unused (FOR NOW >:D)
    @staticmethod
    def forceQuit():
        global prc
        try:
            prc.kill()
            prc = ""
        except:
            pass

    # Fires whe the launcher is closed.
    def closeEvent(self, event):
        global checkAliveTimer
        # Deletes the tmp folder. Gotta keep those directories clean!
        if os.path.exists(config.MC_DIR + "/tmp"):
            shutil.rmtree(config.MC_DIR + "/tmp")
        checkAliveTimer.cancel()
        self.pres.close()
        try:
            instanceWindow.loop.close()
        except:
            pass


# The option window. (Duh!)
class optionWindow(QDialog):
    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        mainWindow.instanceConfig = utils.loadInstanceSettings(mainWindow, mainWindow.currentInstance)
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Options"
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - (480 / 2)
        self.top = screen_resolution.height() / 2 - (240 / 2)
        self.initUI()

    # Same drill. Does visible things.
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 480, 240)
        self.setFixedSize(self.size())
        self.createLabels()
        self.createSettingInputs()

    # Same drill. Creates things.
    def createSettingInputs(self):
        global launcherConfig
        self.javaArgs = QLineEdit(self, text=mainWindow.instanceConfig["javaargs"])
        self.javaArgs.resize(310, 24)
        self.javaArgs.move(150, 20)

        self.maxRamAllocation = QLineEdit(self, text=mainWindow.instanceConfig["maxram"])
        self.maxRamAllocation.resize(100, 24)
        self.maxRamAllocation.move(255, 48)

        self.minRamAllocation = QLineEdit(self, text=mainWindow.instanceConfig["minram"])
        self.minRamAllocation.resize(100, 24)
        self.minRamAllocation.move(360, 48)

    def createLabels(self):
        self.javaArgsLabel = QLabel(self, text="Java arguments:")
        self.javaArgsLabel.resize(100, 20)
        self.javaArgsLabel.move(20, 22)

        self.ramAllocationLabel = QLabel(self, text="RAM Allocation:")
        self.ramAllocationLabel.resize(100, 20)
        self.ramAllocationLabel.move(20, 50)

        self.maxRamAllocationLabel = QLabel(self, text="Maximum:")
        self.maxRamAllocationLabel.move(150, 50)
        self.maxRamAllocationLabel.resize(100, 20)

        self.minRamAllocationLabel = QLabel(self, text="Minimum:")
        self.minRamAllocationLabel.move(310, 50)
        self.minRamAllocationLabel.resize(100, 20)

    # Fires when options window is closed.
    def closeEvent(self, event, *args, **kwargs):
        # Saves config to file.
        mainWindow.instanceConfig["javaargs"] = self.javaArgs.text()
        mainWindow.instanceConfig["minram"] = self.minRamAllocation.text()
        mainWindow.instanceConfig["maxram"] = self.maxRamAllocation.text()
        utils.saveInstanceSettings(mainWindow.instanceConfig, mainWindow.currentInstance)


# Magic! This is how you install modpacks and delete instances.
class instanceWindow(QDialog):
    widgets = []
    progressWin = None
    installModpack = utils.installModpack()
    getModpackFS = utils.getModpackFS()
    getModpackURL = utils.getModpackURL()

    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.getModpackFS.installModpack.connect(self.installModpackWrapper)
        self.getModpackURL.installModpack.connect(self.installModpackWrapper)
        self.installModpack.done.connect(self.modpackInstallDone)
        self.getModpackFS.starting.connect(self.installModpackCockblock)
        self.getModpackURL.starting.connect(self.installModpackCockblock)
        self.installModpack.starting.connect(self.installModpackCockblock)
        optionWindow.launcherConfig = utils.loadSettings(self)
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Instance Manager"
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - 290
        self.top = screen_resolution.height() / 2 - 170
        self.initUI()

    # Same drill. Does showy things.
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 580, 340)
        self.setFixedSize(self.size())
        self.listInstances()
        self.createButtons()
        self.createStatus()
        self.createInput()
        self.status.changed.connect(self.updateIStatus)

    # I sorta figured this out. Still hella bad. Will be sorted sometime in the future.
    def listInstances(self):
        for widget in self.widgets:
            try:
                widget.deleteLater()
            except:
                pass
        self.widgets = []
        self.tab = QTabWidget(self)
        self.tab.move(1, 0)
        self.tab.resize(self.size())
        self.tab.resize(self.tab.width(), self.tab.height()-20)
        self.removeInstanceContainer = QVBoxLayout(self)
        self.removeModpackContainer = QVBoxLayout(self)
        self.installModpackContainer = QVBoxLayout(self)
        self.addInstanceTab = QWidget()
        self.removeInstanceTab = QWidget()
        self.installModpackTab = QWidget()
        self.removeModpackTab = QWidget()
        self.tab.addTab(self.addInstanceTab, "Install Modpacks")
        self.tab.addTab(self.removeInstanceTab, "Delete Instances")
        self.tab.addTab(self.installModpackTab, "Install Cached Modpacks")
        self.tab.addTab(self.removeModpackTab, "Delete Cached Modpacks")
        self.removeInstanceTab.setLayout(self.removeInstanceContainer)
        self.removeModpackTab.setLayout(self.removeModpackContainer)
        self.installModpackTab.setLayout(self.installModpackContainer)

        scroll = QScrollArea(self)
        self.removeInstanceContainer.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.resize(scroll.width(), scroll.height()-20)
        scrollContent = QWidget(scroll)
        self.removeInstanceLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.removeInstanceLayout)
        scroll.setWidget(scrollContent)

        scroll = QScrollArea(self)
        self.removeModpackContainer.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        self.removeModpackLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.removeModpackLayout)
        scroll.setWidget(scrollContent)

        scroll = QScrollArea(self)
        self.installModpackContainer.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        self.installModpackLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.installModpackLayout)
        scroll.setWidget(scrollContent)

        self.updateInstanceList()

    def updateIStatus(self):
        try:
            self.progressWin.status.insertPlainText(self.status.text() + "\n")
        except:
            pass

    def updateInstanceList(self):
        for widget in self.widgets:
            widget.deleteLater()

        self.widgets = []

        instances = [f for f in os.listdir(config.MC_DIR + "/instances") if not os.path.isfile(config.MC_DIR + "/instances/" + f)]
        for instance in instances:
            widget = QPushButton(self, text="Delete " + instance + ".")
            widget.clicked.connect(functools.partial(utils.rmInstance, instance, widget, self))
            self.removeInstanceLayout.addWidget(widget)
            self.widgets.append(widget)

        utils.areYouThere(config.MC_DIR + "/modpackzips")
        modpacks = [f for f in os.listdir(config.MC_DIR + "/modpackzips") if os.path.isfile(config.MC_DIR + "/modpackzips/" + f)]
        for modpack in modpacks:
            widget = QPushButton(self, text="Delete " + modpack + ".")
            widget.clicked.connect(functools.partial(utils.rmModpack, modpack, widget, self))
            self.removeModpackLayout.addWidget(widget)
            self.widgets.append(widget)

        utils.areYouThere(config.MC_DIR + "/modpackzips")
        modpacks = [f for f in os.listdir(config.MC_DIR + "/modpackzips") if os.path.isfile(config.MC_DIR + "/modpackzips/" + f) and (config.MC_DIR + "/modpackzips/" + f).endswith(".zip")]
        for modpack in modpacks:
            widget = QPushButton(self, text="Install " + modpack + ".")
            widget.clicked.connect(functools.partial(self.installModpackWrapper, self, os.path.splitext(modpack)[0]))
            self.installModpackLayout.addWidget(widget)
            self.widgets.append(widget)

    def createButtons(self):
        # Local fylesystem crap
        self.installModpackButton = QPushButton("Install Local Modpack", self.addInstanceTab)
        self.installModpackButton.resize(150, 22)
        self.installModpackButton.move(5, 5)
        self.installModpackButton.clicked.connect(lambda: self.getModpackFSWrapper(self, self.modpackZipDir.text()))

        self.getDirButton = QPushButton("...", self.addInstanceTab)
        self.getDirButton.resize(24, 22)
        self.getDirButton.move(545, 5)
        self.getDirButton.clicked.connect(self.getDir)

        self.openDirButton = QPushButton("Open " + config.NAME + " Install Dir", self.addInstanceTab)
        self.openDirButton.resize(150, 22)
        self.openDirButton.move(5, self.height()-70)
        self.openDirButton.clicked.connect(self.openDir)

        self.openDirButton = QLabel("Automated instance creation comming soon(tm)!", self.addInstanceTab)
        self.openDirButton.move(160, self.height()-170)

        # Url crap
        self.installModpackUrlButton = QPushButton("Install Modpack from URL", self.addInstanceTab)
        self.installModpackUrlButton.resize(150, 22)
        self.installModpackUrlButton.move(5, 34)
        self.installModpackUrlButton.clicked.connect(lambda: self.getModpackURLWrapper(self, self.modpackURL.text()))

    def createStatus(self):
        self.status = utils.status(self)
        self.status.resize(self.width(), 20)
        self.status.move(0, self.height()-20)
        self.updateStatus()

    def createInput(self):
        self.modpackZipDir = QLineEdit(self.addInstanceTab)
        self.modpackZipDir.resize(390, 22)
        self.modpackZipDir.move(155, 5)

        self.modpackURL = QLineEdit(self.addInstanceTab)
        self.modpackURL.resize(390, 22)
        self.modpackURL.move(155, 34)

    def installModpackCockblock(self):
        try:
            if self.progressWin.iWantToDie:
                self.progressWin = installWindow(self)
                self.progressWin.exec_()
        except AttributeError:
            self.progressWin = installWindow(self)
            self.progressWin.exec_()

    def getModpackFSWrapper(self, win, modpackDir):
        self.getModpackFS.modpackDir = modpackDir
        self.getModpackFS.win = win
        self.getModpackFS.start()

    def getModpackURLWrapper(self, win, modpackURL):
        self.getModpackURL.modpackURL = modpackURL
        self.getModpackURL.win = win
        self.getModpackURL.start()

    def installModpackWrapper(self, win, modpackName):
        self.installModpack.modpackName = modpackName
        self.installModpack.win = win
        self.installModpack.start()

    def modpackInstallDone(self):
        self.progressWin.iWantToDie = True
        self.progressWin.close()
        self.updateInstanceList()

    @staticmethod
    def openDir():
        if platform.system() == "Windows":
            os.startfile(config.MC_DIR)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", config.MC_DIR])
        else:
            subprocess.Popen(["xdg-open", config.MC_DIR])

    def getDir(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a Modpack ZIP File", os.path.expanduser("~"), "Modpack ZIP Archive (*.zip)")
        if fileName:
            self.modpackZipDir.setText(fileName)

    # Cause we need an error box thingy without too much copypasta.
    def error(self, err):
        QMessageBox.warning(self, "Warning", err, QMessageBox.Ok, QMessageBox.Ok)

    def updateStatus(self, text="", color="black", bgcolor="lightgrey"):
        self.status.setLabelText(text)
        self.status.setStyleSheet("color: " + color + "; background-color: " + bgcolor + ";")

    # Fires when the instance select window closes.
    def closeEvent(self, event, *args, **kwargs):
        global mainWin
        # Wouldnt want to try and launch a non-existant instance now, do we?
        if not os.path.exists(config.MC_DIR + "/instances/" + mainWindow.currentInstance):
            try:
                mainWindow.currentInstance = os.listdir(config.MC_DIR + "/instances")[0]
            except:
                mainWindow.currentInstance = ""

        mainWindow.setInstance(mainWin, mainWindow.currentInstance)
        mainWindow.createDropdowns(mainWin)


class installWindow(QDialog):
    iWantToDie = False

    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Modpack Installer"
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - 200
        self.top = screen_resolution.height() / 2 - 220
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 200, 220)
        self.setFixedSize(self.size())
        self.createLabel()
        self.createStatus()

    def createLabel(self):
        self.label = QLabel(self, text="Installing modpack...")
        self.label.move(5, 5)
        self.label.resize(self.width()/2, 22)
        self.label.setStyleSheet("text-align: center;")

    def createStatus(self):
        self.status = QTextEdit(self)
        self.status.setReadOnly(True)
        self.status.move(5, 27)
        self.status.resize(self.width()-10, self.height()-32)

    def closeEvent(self, event, *args, **kwargs):
        if not self.iWantToDie:
            event.ignore()


if __name__ == '__main__':
    try:
        mainWindow.currentInstance = os.listdir(config.MC_DIR + "/instances")[0]
    except:
        mainWindow.currentInstance = ""

    update = True
    prc = ""
    running = False

    threadingEvent = threading.Event()

    app = QApplication(sys.argv)
    mainWin = mainWindow()

    sys.exit(app.exec_())
