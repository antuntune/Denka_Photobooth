from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from cloudinary.uploader import upload
import json
import time
import cloudinary

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
        self.qr = self.findChild(QtWidgets.QLabel, 'qr')
        qrPixmap = QPixmap(
            'res/event/' + eventId + '/qr.png')
        self.qr.setPixmap(qrPixmap)
        # link
        self.link = self.findChild(QtWidgets.QLabel, 'link')
        self.link.setText("djenka.tk/"+eventId)
        # slike
        self.img1 = self.findChild(QtWidgets.QLabel, 'img1')
        self.img2 = self.findChild(QtWidgets.QLabel, 'img2')
        self.img3 = self.findChild(QtWidgets.QLabel, 'img3')

        # radio
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio1"))
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio3"))
        # button
        self.pushButton.clicked.connect(self.sharePressed)
        self.skipButton.clicked.connect(self.skipPressed)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:

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
