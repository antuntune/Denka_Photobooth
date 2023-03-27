
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import json

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']


class CameraUi(QMainWindow):
    def __init__(self):
        super(CameraUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/camera.ui", self)

        self.strip = self.findChild(QtWidgets.QLabel, 'strip')
        stripPixmap = QPixmap(
            'res/event/' + eventId + '/kartica.png')
        self.strip.setPixmap(stripPixmap)

        self.cardSlot1 = self.findChild(QtWidgets.QLabel, 'img1')
        self.cardSlot2 = self.findChild(QtWidgets.QLabel, 'img2')
        self.cardSlot3 = self.findChild(QtWidgets.QLabel, 'img3')

        img1pixmap = QPixmap('res/session/slika1.jpg')
        img2pixmap = QPixmap('res/session/slika2.jpg')
        img3pixmap = QPixmap('res/session/slika3.jpg')

        self.cardSlot1.setPixmap(img1pixmap)
        self.cardSlot2.setPixmap(img2pixmap)
        self.cardSlot3.setPixmap(img3pixmap)

        self.pushButton.clicked.connect(self.changeToPrintUi)

    def changeToPrintUi(self):
        self.parent().setCurrentIndex(2)
