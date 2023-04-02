from PyQt5.QtWidgets import QMainWindow, QLabel, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
import json
import cloudinary
import time
from cloudinary.uploader import upload

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']

cloudinary.config(
    cloud_name="dpuhwc49z",
    api_key="544431793628367",
    api_secret="jXcv2cki8LffeJ1Wz-FOrYU4sd8",
    secure=True
)


class AlbumUi(QMainWindow):
    def __init__(self):
        super(AlbumUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/album.ui", self)

        # qr kod
        self.qr = self.findChild(QLabel, 'qr')
        qrPixmap = QPixmap(
            'res/event/' + eventId + '/qr.png')
        self.qr.setPixmap(qrPixmap)
        # link
        self.link = self.findChild(QLabel, 'link')
        self.link.setText("djenka.tk/"+eventId)
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
        self.btn_sfx.setSource(QUrl.fromLocalFile('res/ui/btn.wav'))
        self.pushButton.pressed.connect(self.btn_sfx.play)

        # button
        self.pushButton.clicked.connect(self.sharePressed)
        self.skipButton.clicked.connect(self.skipPressed)

    def showEvent(self, a0: QShowEvent) -> None:

        img1pixmap = QPixmap('res/session/slika1.jpg')
        img2pixmap = QPixmap('res/session/slika2.jpg')
        img3pixmap = QPixmap('res/session/slika3.jpg')
        self.img1.setPixmap(img1pixmap)
        self.img2.setPixmap(img2pixmap)
        self.img3.setPixmap(img3pixmap)

        return super().showEvent(a0)

    def sharePressed(self):
        # provjerava koji je radiobutton ukljucen
        if self.buttonGroup.checkedId() == -2:
            brojSlike = 1
        elif self.buttonGroup.checkedId() == -3:
            brojSlike = 2
        elif self.buttonGroup.checkedId() == -4:
            brojSlike = 3

        self.uploadToAlbum(brojSlike, eventId)

        self.parent().setCurrentIndex(1)

    def skipPressed(self):
        self.parent().setCurrentIndex(1)

    def uploadToAlbum(self, brojSlike, eventId):
        upload("res/session/slika" + str(brojSlike) + ".jpg",
               public_id="djenka/" + eventId + "/album/" + str(time.time()))
