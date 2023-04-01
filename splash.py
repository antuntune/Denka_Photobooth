from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
import json

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']


class SplashUi(QMainWindow):
    def __init__(self):
        super(SplashUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/splash.ui", self)

        # qr kod
        self.qr = self.findChild(QLabel, 'qr')
        qrPixmap = QPixmap(
            'res/event/' + eventId + '/qr.png')
        self.qr.setPixmap(qrPixmap)
        # link
        self.link = self.findChild(QLabel, 'link')
        self.link.setText("djenka.tk/"+eventId)
        # Button sound effect
        self.btn_sfx = QSoundEffect()
        self.btn_sfx.setSource(QUrl.fromLocalFile('res/ui/btn.wav'))
        self.pushButton.pressed.connect(self.btn_sfx.play)

        self.pushButton.clicked.connect(self.buttonPressed)

    def buttonPressed(self):

        self.parent().setCurrentIndex(2)
