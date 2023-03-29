
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import json
from PIL import Image

import cv2
import os
import keyboard

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

        self.pushButton.clicked.connect(self.changeToPrintUi)

    def changeToPrintUi(self):
        self.parent().setCurrentIndex(3)

    def napraviKarticu(self, eventId):

        kartica = Image.open('res/event/'+eventId+'/kartica.png')
        im1 = Image.open('res/session/slika1.jpg').resize((800, 533))
        im2 = Image.open('res/session/slika2.jpg').resize((800, 533))
        im3 = Image.open('res/session/slika3.jpg').resize((800, 533))

        kartica.paste(im1, (100, 187))
        kartica.paste(im2, (100, 877))
        kartica.paste(im3, (100, 1567))

        kartica.save('res/session/gotovaKartica.png')

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.count = 1

        keyboard.add_hotkey('k', lambda: self.slikaj())

        return super().showEvent(a0)

    def slikaj(self):

        # Set up camera
        cap = cv2.VideoCapture(0)

        # Capture image from camera
        ret, frame = cap.read()

        # Save image to disk
        filename = f'res/session/slika{self.count}.jpg'
        cv2.imwrite(filename, frame)

        # Print message to console
        print(f'Image {self.count} saved to {filename}')

        if self.count == 1:
            img1pixmap = QPixmap('res/session/slika1.jpg')
            self.cardSlot1.setPixmap(img1pixmap)
        elif self.count == 2:
            img2pixmap = QPixmap('res/session/slika2.jpg')
            self.cardSlot2.setPixmap(img2pixmap)
        elif self.count == 3:
            img3pixmap = QPixmap('res/session/slika3.jpg')
            self.cardSlot3.setPixmap(img3pixmap)

        # Increment count
        self.count += 1

        if self.count > 3:
            keyboard.unhook_all_hotkeys()
            self.napraviKarticu(eventId)
