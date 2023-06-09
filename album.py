from PyQt5.QtWidgets import QMainWindow, QLabel, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QUrl
from PyQt5.QtMultimedia import QSoundEffect
import json
import cloudinary
import time, os
from cloudinary.uploader import upload
import importlib
import threading



cloudinary.config(
    cloud_name="dpuhwc49z",
    api_key="544431793628367",
    api_secret="jXcv2cki8LffeJ1Wz-FOrYU4sd8",
    secure=True
)


class TimeOutThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        time.sleep(25)
        self.finished.emit()  # Emit the 'finished' signal when the work is done


class AlbumUi(QMainWindow):
    def __init__(self):
        super(AlbumUi, self).__init__()

        self.loaded_resources = False
        self.skipButtonPressed = False

        self.brojSlike = 1
        self.eventId = ""

        self.uploadThread = threading.Thread(target = self.uploadToAlbum, args=(self.brojSlike, self.eventId))

        self.timeout_thread = TimeOutThread(parent=self)
        self.timeout_thread.finished.connect(self.timeoutThreadFinished)

    def timeoutThreadFinished(self):
        if self.skipButtonPressed == False:
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

        uic.loadUi(os.getcwd() + "/res/ui/"+self.tema+"/album.ui", self)

        # qr kod
        self.qr = self.findChild(QLabel, 'qr')
        qrPixmap = QPixmap(self.albumPath + self.eventId + "/qr.png")
        self.qr.setPixmap(qrPixmap)
        # link
        self.link = self.findChild(QLabel, 'link')
        self.link.setText("denka.live/"+self.eventId)
        # slike
        self.img1 = self.findChild(QLabel, 'img1')
        self.img2 = self.findChild(QLabel, 'img2')
        self.img3 = self.findChild(QLabel, 'img3')

        # radio
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio1"))
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio3"))

        # Button sound effect
        self.btn_sfx = QSoundEffect()
        self.btn_sfx.setSource(QUrl.fromLocalFile(os.getcwd() + '/res/ui/btn.wav'))
        self.pushButton.pressed.connect(self.btn_sfx.play)

        # button
        self.pushButton.clicked.connect(self.sharePressed)
        self.skipButton.clicked.connect(self.skipPressed)

    def showEvent(self, a0: QShowEvent) -> None:

        if not self.loaded_resources:
            self.loadFromJson()
            self.loadResources()
            self.loaded_resources = True

        self.skipButtonPressed = False

        img1pixmap = QPixmap(self.eventAlbumPath + "slika1.jpg")
        img2pixmap = QPixmap(self.eventAlbumPath + "slika2.jpg")
        img3pixmap = QPixmap(self.eventAlbumPath + "slika3.jpg")
        self.img1.setPixmap(img1pixmap)
        self.img2.setPixmap(img2pixmap)
        self.img3.setPixmap(img3pixmap)

        self.timeout_thread.start()

        return super().showEvent(a0)

    def sharePressed(self):
        # provjerava koji je radiobutton ukljucen
        if self.buttonGroup.checkedId() == -2:
            self.brojSlike = 1
        elif self.buttonGroup.checkedId() == -3:
            self.brojSlike = 2
        elif self.buttonGroup.checkedId() == -4:
            self.brojSlike = 3

        
        #self.uploadThread.start()

        self.uploadToAlbum(brojSlike, self.eventId)

        self.skipButtonPressed = True

        self.parent().setCurrentIndex(1)

    def skipPressed(self):
        self.skipButtonPressed = True
        self.parent().setCurrentIndex(1)

    def uploadToAlbum(self, brojSlike, eventId):
        upload(self.eventAlbumPath + "slika" + str(brojSlike) + ".jpg",
               public_id="djenka/" + self.eventId + "/album/" + str(time.time()))


