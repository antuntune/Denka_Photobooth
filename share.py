from PyQt5.QtWidgets import QMainWindow, QLabel, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QUrl
from PyQt5.QtMultimedia import QSoundEffect
import json
import time, os
import importlib
import threading



class TimeOutThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        time.sleep(120)  # Timeout for splash screen
        self.finished.emit()  # Emit the 'finished' signal when the work is done


class ShareUi(QMainWindow):
    def __init__(self):
        super(ShareUi, self).__init__()

        self.loaded_resources = False

        self.timeout_thread = TimeOutThread(parent=self)
        self.timeout_thread.finished.connect(self.timeoutThreadFinished)

    def timeoutThreadFinished(self):

        self.parent().setCurrentIndex(1)

    def loadFromJson(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('config.json', 'r') as f:
            # Load the contents of the file into a dictionary
            config = json.load(f)
            self.eventId = config['eventId']
            self.tema = config['tema']
            self.albumPath = config['albumPath']
            self.eventAlbumPath = config['eventAlbumPath']
            self.cardPath = config['cardPath']

    def loadResources(self):

        uic.loadUi(os.getcwd() + "/res/ui/"+self.tema+"/share.ui", self)

        # qr kod
        self.qr = self.findChild(QLabel, 'qr')
        qrPixmap = QPixmap(self.albumPath + self.eventId + "/qr.png")
        self.qr.setPixmap(qrPixmap)

        # Button sound effect
        self.btn_sfx = QSoundEffect()
        self.btn_sfx.setSource(QUrl.fromLocalFile(os.getcwd() + '/res/ui/btn.wav'))
        self.skipButton.pressed.connect(self.btn_sfx.play)

        # button
        self.skipButton.clicked.connect(self.skipPressed)

        # Load the image file into a QPixmap
        pixmap = QPixmap("shareQR.png")  # Replace "image.jpg" with your image file

        # Set the scale factor of the QPixmap to match the size of the QLabel
        pixmap = pixmap.scaled(self.qr.size(), aspectRatioMode=True)

        # Set the QPixmap object to the QLabel
        self.qr.setPixmap(pixmap)

    def showEvent(self, a0: QShowEvent) -> None:

        if not self.loaded_resources:
            self.loadFromJson()
            self.loadResources()
            self.loaded_resources = True

        self.timeout_thread.start()

        self.readPIN()

        return super().showEvent(a0)

    def readPIN(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('pin.json', 'r') as f:
            # Load the contents of the file into a dictionary
            pin = json.load(f)
        self.sessionPin = pin['PIN']
        self.pin.setText("PIN: " + str(self.sessionPin))
        print("Label Pin", self.sessionPin)

    def skipPressed(self):

        # kill timeout thread which set up splash window if timeout happend beacuse skip button is pressed
        self.timeout_thread.terminate()

        self.parent().setCurrentIndex(1)




