import config
import utils
import os
import sys
import requests

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QCheckBox, QApplication

class exportWindow(QWidget):
    currentInstance = ""

    # Same drill. Does background things.
    def __init__(self, parent=None):
        super().__init__(parent)
        screen_resolution = app.desktop().screenGeometry()
        self.title = config.NAME + " " + config.VER + " Modpack Installer"
        config.ICON = utils.loadImage("favicon.ico", self.currentInstance)
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

        self.createModpackButton = QPushButton(self)
        self.createModpackButton.clicked.connect(self.createModpack)
        self.createModpackButton.setText("Export Modpack")
        self.createModpackButton.move(50, 50)

    def createCheckBoxes(self):
        self.doDefaultSoundRemoval = QCheckBox(self)
        self.doDefaultSoundRemoval.move(100, 20)
        self.doDefaultSoundRemoval.clicked.connect(lambda: print(self.doDefaultSoundRemoval.isChecked()))

    def createModpack(self):
        soundsMD5 = self.getSoundXML()
        print(soundsMD5)

    # Screw XML. It's terrible. I chose to use it because I only had to add a single 10 character line to my minecraft resources php file. Fight me.
    @staticmethod
    def getSoundXML():
        md5Array = []
        with requests.get("http://resourceproxy.pymcl.net/MinecraftResources") as response:
            trip = False
            for string in response.text.split("<Key>"):
                if trip:
                    md5Array.append([string.split("</Key>")[0], string.split("<MD5>")[1].split("</MD5>")[0]])
                else:
                    trip = True

        return md5Array

    def md5Recursive(self, pathininstance):
        for root, dirs, files in os.walk(config.MC_DIR + "/" + self.currentInstance + "/" + pathininstance):
            for file in files:
                utils.md5(root + "/" + file)


app = QApplication([])
exportWin = exportWindow()

sys.exit(app.exec_())
