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
import asyncio

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QPushButton, QWidget, QComboBox, QLineEdit, QLabel, QMessageBox, QDialog, QCheckBox, QVBoxLayout, QGroupBox, QTextBrowser, QTabWidget, QScrollArea, QFileDialog, QApplication, QTextEdit


class mainWindow(QWidget):
    guiElements = []
    dirt = []
    guiMove = []
    instanceSelect = ""
    creds = ""

    # This is used to init the background crap such as update checking and rich presence.
    def __init__(self):
        super().__init__()
        try:
            self.currentInstance = os.listdir(config.MC_DIR + "/instances")[0]
        except:
            self.currentInstance = ""
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
        self.update = utils.checkOnline()
        self.initUI()

    # This sets up all the crap you see.
    def initUI(self):
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
            self.creds = " --username=" + self.loginBox.text()
            self.launch()

        self.loginButton.setText("Force Quit")
        self.loginButton.disconnect()
        self.loginButton.clicked.connect(self.forceQuit)
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
            item = ""
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
        self.theInternet = QTextBrowser(self)
        with open(config.BLOG, "r", encoding="utf-8") as file:
            content = file.read()
        self.theInternet.setHtml(content.replace("&background&", urllib.parse.quote(config.BLOG_BACKGROUND.replace("\\", "/"))))
        self.theInternet.setOpenExternalLinks(True)
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
        global checkAliveTimer, running
        try:
            poll = self.prc.poll()
            if poll is None:
                running = True
            else:
                try:
                    self.proxy.stop()
                except:
                    pass
                raise AttributeError
        except AttributeError:
            try:
                # Enables all the buttons so they can be used again.
                self.loginButton.setText("Login")
                self.loginButton.disconnect()
                self.loginButton.clicked.connect(self.login)
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
        try:
            self.prc.kill()
        except:
            pass
        try:
            self.proxy.stop()
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

            self.proxiedArgs = self.instanceConfig["javaargs"]

            if self.instanceConfig["proxyskin"] or self.instanceConfig["proxysound"] or self.instanceConfig["proxycape"]:

                self.proxy = utils.minecraftProxy(doSkinFix=self.instanceConfig["proxyskin"], doSoundFix=self.instanceConfig["proxysound"], doCapeFix=self.instanceConfig["proxycape"], loop=asyncio.new_event_loop())
                self.proxy.start()
                self.proxiedArgs += " -Dhttp.proxyHost=localhost -Dhttp.proxyPort=25560 -Dhttps.proxyHost=localhost -Dhttps.proxyPort=25560"

            # Overrides all references to %appdata%, $user.home and $home
            os.environ["APPDATA"] = config.MC_DIR + "/instances/" + self.currentInstance
            os.environ["USER.HOME"] = config.MC_DIR + "/instances/" + self.currentInstance
            os.environ["HOME"] = config.MC_DIR + "/instances/" + self.currentInstance

            # Launch the game. I ONLY DEAL IN ABSOLUTES.
            print("java " + self.proxiedArgs + " -Xms" + self.instanceConfig["minram"] + " -Xmx" + self.instanceConfig["maxram"] + " -jar \"" + utils.resourcePath("EasyMineLauncher.jar") + "\" --lwjgl-dir=\"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft/bin" + "\" --jar=\"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft/bin/minecraft.jar" + "\" --native-dir=\"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft" + "/bin/natives\"" + " --height=520 --width=870 --x=" + str(int((app.desktop().screenGeometry().width() / 2) - 435)) + " --y=" + str(int((app.desktop().screenGeometry().height() / 2) - 270)) + self.creds)
            self.prc = subprocess.Popen("java " + self.proxiedArgs + " -Xms" + self.instanceConfig["minram"] + " -Xmx" + self.instanceConfig["maxram"] + " -jar \"" + utils.resourcePath("EasyMineLauncher.jar") + "\" --lwjgl-dir=\"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft/bin" + "\" --jar=\"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft/bin/minecraft.jar" + "\" --native-dir=\"" + config.MC_DIR + "/instances/" + self.currentInstance + "/.minecraft" + "/bin/natives\"" + " --height=520 --width=870 --x=" + str(int((app.desktop().screenGeometry().width() / 2) - 435)) + " --y=" + str(int((app.desktop().screenGeometry().height() / 2) - 270)) + self.creds, env=dict(os.environ))

            self.launcherConfig["lastusedname"] = self.loginBox.text()
            utils.saveSettings(self.launcherConfig)
            try:
                self.pres.update(details="Playing", large_image="pymcllogo512", state="Selected modpack: " + self.currentInstance)
            except:
                pass
            self.loggedIn = False
            self.proxiedArgs = ""
        except Exception as e:
            # Tragic.
            self.error("Minecraft is unable to start. Make sure you have java and minecraft installed and an alphanumeric username set.")
            print("Rejected username: " + self.loginBox.text())
            print(e)

    # Cause we need an error box thingy without too much copypasta.
    def error(self, err):
        QMessageBox.warning(self, "Warning", err, QMessageBox.Ok, QMessageBox.Ok)

    def forceQuit(self):
        try:
            self.proxy.stop()
            self.proxy = ""
        except:
            pass
        try:
            self.prc.kill()
            self.prc = ""
        except:
            pass

    # Fires whe the launcher is closed.
    def closeEvent(self, event):
        global checkAliveTimer
        checkAliveTimer.cancel()
        try:
            self.pres.close()
        except:
            pass
        try:
            instanceWindow.loop.close()
        except:
            pass

        # Deletes the tmp folder. Gotta keep those directories clean!
        if os.path.exists(config.MC_DIR + "/tmp"):
            shutil.rmtree(config.MC_DIR + "/tmp")


# The option window. (Duh!)
class optionWindow(QDialog):
    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        mainWin.instanceConfig = utils.loadInstanceSettings(mainWin, mainWin.currentInstance)
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
        self.javaArgs = QLineEdit(self, text=mainWin.instanceConfig["javaargs"])
        self.javaArgs.resize(310, 24)
        self.javaArgs.move(150, 20)

        self.maxRamAllocation = QLineEdit(self, text=mainWin.instanceConfig["maxram"])
        self.maxRamAllocation.resize(100, 24)
        self.maxRamAllocation.move(255, 48)

        self.minRamAllocation = QLineEdit(self, text=mainWin.instanceConfig["minram"])
        self.minRamAllocation.resize(100, 24)
        self.minRamAllocation.move(360, 48)

        self.enableAutoProxySkin = QCheckBox(self)
        self.enableAutoProxySkin.setChecked(mainWin.instanceConfig["proxyskin"])
        self.enableAutoProxySkin.move(150, 81)

        self.enableAutoProxySound = QCheckBox(self)
        self.enableAutoProxySound.setChecked(mainWin.instanceConfig["proxysound"])
        self.enableAutoProxySound.move(150, 109)

        self.enableAutoProxyCape = QCheckBox(self)
        self.enableAutoProxyCape.setChecked(mainWin.instanceConfig["proxycape"])
        self.enableAutoProxyCape.move(150, 137)

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

        self.enableAutoProxySkinLabel = QLabel(self, text="Enable skin proxy:")
        self.enableAutoProxySkinLabel.resize(100, 20)
        self.enableAutoProxySkinLabel.move(20, 76)

        self.enableAutoProxySoundLabel = QLabel(self, text="Enable sound proxy:")
        self.enableAutoProxySoundLabel.resize(100, 20)
        self.enableAutoProxySoundLabel.move(20, 104)

        self.enableAutoProxyCapeLabel = QLabel(self, text="Enable cape proxy:")
        self.enableAutoProxyCapeLabel.resize(100, 20)
        self.enableAutoProxyCapeLabel.move(20, 132)

        self.enableAutoProxySkinLabel2 = QLabel(self, text="(Breaks sounds if skinfix is installed!)")
        self.enableAutoProxySkinLabel2.resize(250, 20)
        self.enableAutoProxySkinLabel2.move(170, 76)

        self.enableAutoProxySoundLabel2 = QLabel(self, text="(Backup your resources folder if using custom sounds!)")
        self.enableAutoProxySoundLabel2.resize(300, 20)
        self.enableAutoProxySoundLabel2.move(170, 104)

        self.enableAutoProxyCapeLabel2 = QLabel(self, text="(Breaks sounds if skinfix is installed!)")
        self.enableAutoProxyCapeLabel2.resize(250, 20)
        self.enableAutoProxyCapeLabel2.move(170, 132)

    # Fires when options window is closed.
    def closeEvent(self, event, *args, **kwargs):
        # Saves config to file.
        mainWin.instanceConfig["javaargs"] = self.javaArgs.text()
        mainWin.instanceConfig["minram"] = self.minRamAllocation.text()
        mainWin.instanceConfig["maxram"] = self.maxRamAllocation.text()
        mainWin.instanceConfig["proxyskin"] = self.enableAutoProxySkin.isChecked()
        mainWin.instanceConfig["proxysound"] = self.enableAutoProxySound.isChecked()
        mainWin.instanceConfig["proxycape"] = self.enableAutoProxyCape.isChecked()
        utils.saveInstanceSettings(mainWin.instanceConfig, mainWin.currentInstance)


# Magic! This is how you install modpacks and delete instances.
class instanceWindow(QDialog):
    widgets = []
    repoWidgets = []
    installModpack = utils.installModpack()
    getModpackFS = utils.getModpackFS()
    getModpackURL = utils.getModpackURL()
    getModpackRepo = utils.getModpackRepo()

    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progressWin = installWindow(self)
        self.getModpackRepo.result.connect(self.updateRepo)
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
        self.show()
        self.getModpackRepo.start()

    def updateRepo(self, result, modpacks):
        for widget in self.repoWidgets:
            try:
                widget.deleteLater()
            except:
                pass

        self.repoWidgets = []

        if result == True:
            for key, modpack in modpacks["modpacks"].items():
                vbox = QVBoxLayout()
                group = QGroupBox(modpack["name"] + " version " + modpack["modpackver"])
                widget = QPushButton(self, text="Install " + modpack["name"] + " version " + modpack["modpackver"] + ".")
                widget1 = QTextEdit(self)
                widget2 = QPushButton(self, text="View on pymcl.net")
                widget1.setText(modpack["smalldesc"])
                widget1.setReadOnly(True)
                widget.clicked.connect(functools.partial(self.getModpackURLWrapper, modpack["zipurl"]))
                widget2.clicked.connect(functools.partial(utils.openModpackInBrowser, key))
                vbox.addWidget(widget)
                vbox.addWidget(widget1)
                vbox.addWidget(widget2)
                group.setLayout(vbox)
                self.modpackRepoLayout.addWidget(group)
                self.repoWidgets.append(widget)
                self.repoWidgets.append(group)

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
        self.modpackRepoContainer = QVBoxLayout(self)
        self.addInstanceTab = QWidget()
        self.removeInstanceTab = QWidget()
        self.installModpackTab = QWidget()
        self.removeModpackTab = QWidget()
        self.modpackRepoTab = QWidget()
        self.tab.addTab(self.addInstanceTab, "Install Modpacks")
        self.tab.addTab(self.modpackRepoTab, "Modpack Repo")
        self.tab.addTab(self.removeInstanceTab, "Delete Instances")
        self.tab.addTab(self.installModpackTab, "Install Cached Modpacks")
        self.tab.addTab(self.removeModpackTab, "Delete Cached Modpacks")
        self.removeInstanceTab.setLayout(self.removeInstanceContainer)
        self.removeModpackTab.setLayout(self.removeModpackContainer)
        self.installModpackTab.setLayout(self.installModpackContainer)
        self.modpackRepoTab.setLayout(self.modpackRepoContainer)

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

        scroll = QScrollArea(self)
        self.modpackRepoContainer.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        self.modpackRepoLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.modpackRepoLayout)
        scroll.setWidget(scrollContent)
        self.refreshButton = QPushButton(self.modpackRepoTab)
        self.refreshButton.move(8, 8)
        self.refreshButton.resize(20, 20)
        icon = QIcon(utils.resourcePath("refresh.png"))
        self.refreshButton.setIcon(icon)
        self.refreshButton.clicked.connect(self.getModpackRepo.start)


        self.updateInstanceList()

    def updateInstanceList(self):
        for widget in self.widgets:
            widget.deleteLater()

        self.widgets = []

        instances = [f for f in os.listdir(config.MC_DIR + "/instances") if not os.path.isfile(config.MC_DIR + "/instances/" + f)]
        for instance in instances:
            widget = QPushButton(self, text="Delete " + instance + ".")
            widget.clicked.connect(functools.partial(utils.rmInstance, instance, self))
            self.removeInstanceLayout.addWidget(widget)
            self.widgets.append(widget)

        utils.areYouThere(config.MC_DIR + "/modpackzips")
        modpacks = [f for f in os.listdir(config.MC_DIR + "/modpackzips") if os.path.isfile(config.MC_DIR + "/modpackzips/" + f)]
        for modpack in modpacks:
            widget = QPushButton(self, text="Delete " + modpack + ".")
            widget.clicked.connect(functools.partial(utils.rmModpack, modpack, self))
            self.removeModpackLayout.addWidget(widget)
            self.widgets.append(widget)

        utils.areYouThere(config.MC_DIR + "/modpackzips")
        modpacks = [f for f in os.listdir(config.MC_DIR + "/modpackzips") if os.path.isfile(config.MC_DIR + "/modpackzips/" + f) and (config.MC_DIR + "/modpackzips/" + f).endswith(".zip")]
        for modpack in modpacks:
            widget = QPushButton(self, text="Install " + modpack + ".")
            widget.clicked.connect(functools.partial(self.installModpackWrapper, os.path.splitext(modpack)[0]))
            self.installModpackLayout.addWidget(widget)
            self.widgets.append(widget)

    def createButtons(self):
        # Local filesystem crap
        self.installModpackButton = QPushButton("Install Local Modpack", self.addInstanceTab)
        self.installModpackButton.resize(150, 22)
        self.installModpackButton.move(5, 5)
        self.installModpackButton.clicked.connect(lambda: self.getModpackFSWrapper(self.modpackZipDir.text()))

        self.getDirButton = QPushButton("...", self.addInstanceTab)
        self.getDirButton.resize(24, 22)
        self.getDirButton.move(545, 5)
        self.getDirButton.clicked.connect(self.getDir)

        self.openDirButton = QPushButton("Open " + config.NAME + " Install Dir", self.addInstanceTab)
        self.openDirButton.resize(150, 22)
        self.openDirButton.move(5, self.height()-70)
        self.openDirButton.clicked.connect(self.openDir)

        self.messageLabel = QLabel("Automated instance creation comming soon(tm)!", self.addInstanceTab)
        self.messageLabel.move(160, self.height()-170)

        # Url crap
        self.installModpackUrlButton = QPushButton("Install Modpack from URL", self.addInstanceTab)
        self.installModpackUrlButton.resize(150, 22)
        self.installModpackUrlButton.move(5, 34)
        self.installModpackUrlButton.clicked.connect(lambda: self.getModpackURLWrapper(self.modpackURL.text()))

    def createStatus(self):
        self.status = QLabel(self)
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

    def progressWinWrapper(self):
        if self.progressWin.iWantToDie == True:
            self.progressWin.iWantToDie = False
            self.progressWin.exec_()

    def modpackInstallDone(self):
        self.progressWin.iWantToDie = True
        self.progressWin.close()
        self.updateInstanceList()



    def installModpackWrapper(self, modpackName):
        self.installModpack.stop()
        self.installModpack = utils.installModpack(modpackName)
        self.installModpack.done.connect(self.modpackInstallDone)
        self.installModpack.starting.connect(self.progressWinWrapper)
        self.installModpack.updateIStatus.connect(self.updateIStatus)
        self.installModpack.updateStatus.connect(self.updateStatus)
        self.installModpack.start()

    def getModpackURLWrapper(self, modpackURL):
        self.getModpackURL.stop()
        self.getModpackURL = utils.getModpackURL(modpackURL)
        self.getModpackURL.starting.connect(self.progressWinWrapper)
        self.getModpackURL.installModpack.connect(self.installModpackWrapper)
        self.getModpackURL.updateIStatus.connect(self.updateIStatus)
        self.getModpackURL.start()

    def getModpackFSWrapper(self, modpackDir):
        self.getModpackFS.stop()
        self.getModpackFS = utils.getModpackFS(modpackDir)
        self.getModpackFS.starting.connect(self.progressWinWrapper)
        self.getModpackFS.installModpack.connect(self.installModpackWrapper)
        self.getModpackFS.start()

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
        self.status.setText(text)
        self.status.setStyleSheet("color: " + color + "; background-color: " + bgcolor + ";")

    def updateIStatus(self, text):
        print(text)
        try:
            if text.startswith("[") and self.progressWin.status.toPlainText().split("\n")[len(self.progressWin.status.toPlainText().split("\n"))-2].startswith("["):
                newtext = self.progressWin.status.toPlainText().split("\n")
                newtext = "\n".join(newtext[:len(newtext)-2])
                newtext = newtext + "\n" + text + "\n"
            else:
                newtext = self.progressWin.status.toPlainText() + text + "\n"
            self.progressWin.status.setText(newtext)
            self.progressWin.status.verticalScrollBar().setValue(self.progressWin.status.verticalScrollBar().maximum())
        except:
            pass


    # Fires when the instance select window closes.
    def closeEvent(self, event, *args, **kwargs):
        global mainWin
        # Wouldnt want to try and launch a non-existant instance now, do we?
        if not os.path.exists(config.MC_DIR + "/instances/" + mainWin.currentInstance):
            try:
                mainWin.currentInstance = os.listdir(config.MC_DIR + "/instances")[1]
            except:
                mainWin.currentInstance = ""

        mainWin.createDropdowns()
        mainWin.setInstance(mainWin.currentInstance)


class installWindow(QDialog):
    iWantToDie = True

    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Modpack Installer"
        self.setWindowIcon(QIcon(config.ICON))
        self.left = screen_resolution.width() / 2 - 450
        self.top = screen_resolution.height() / 2 - 220
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 450, 220)
        self.setFixedSize(self.size())
        self.createLabels()
        self.createStatus()

    def createLabels(self):
        self.label = QLabel(self, text="Installing modpack...")
        self.label.move(5, 5)
        self.label.resize(self.width()/2, 22)
        self.label.setStyleSheet("text-align: center;")

    def createStatus(self):
        self.status = QTextEdit(self)
        self.status.setReadOnly(True)
        self.status.move(5, 27)
        self.status.resize(self.width()-10, self.height()-32)
        font = QFont()
        font.setStyleHint(QFont().Monospace)
        font.setFamily("monospace")
        self.status.setFont(font)

    def closeEvent(self, event, *args, **kwargs):
        if not self.iWantToDie:
            event.ignore()
        else:
            self.status.clear()


# sys.stdout = open(config.MC_DIR + "/" + str(time.time()) + ".log", "w")

threadingEvent = threading.Event()

app = QApplication([])
mainWin = mainWindow()

sys.exit(app.exec_())
