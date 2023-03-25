from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QDialog, QWidget, QStackedWidget, QRadioButton
from PyQt5 import uic, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QDialog, QWidget, QStackedWidget
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread

from PyQt5 import uic

import sys
import time
import datetime
import keyboard


import res

import cloudinary
from cloudinary.uploader import upload

import cups
from PIL import Image

conn = cups.Connection ()
printers = conn.getPrinters ()
# printers is a dictionary containing information about all the printers available

emptyDict = {}
AvailablePrinters = list(printers.keys())
PrinterUsing = AvailablePrinters[0]


cloudinary.config(
    cloud_name="dpuhwc49z",
    api_key="544431793628367",
    api_secret="jXcv2cki8LffeJ1Wz-FOrYU4sd8",
    secure=True
)


class SplashUi(QMainWindow):
    def __init__(self):
        super(SplashUi, self).__init__()
        uic.loadUi("res/ui/splash.ui", self)

        self.pushButton.clicked.connect(self.changeToCameraUi)

    def changeToCameraUi(self):

        widget.setCurrentWidget(CameraUi)


class CameraUi(QMainWindow):
    def __init__(self):
        super(CameraUi, self).__init__()
        uic.loadUi("res/ui/camera.ui", self)

        self.cardSlot1 = self.findChild(QtWidgets.QLabel, 'img1')
        self.cardSlot2 = self.findChild(QtWidgets.QLabel, 'img2')
        self.cardSlot3 = self.findChild(QtWidgets.QLabel, 'img3')

        img1pixmap = QPixmap('res/session/slika1.jpg')
        img2pixmap = QPixmap('res/session/slika2.jpg')
        img3pixmap = QPixmap('res/session/slika3.jpg')

        self.cardSlot1.setPixmap(img1pixmap)
        self.cardSlot2.setPixmap(img2pixmap)
        self.cardSlot3.setPixmap(img3pixmap)

        def daljinskiPritisnut():
            print("k was pressed")

        keyboard.add_hotkey('k', lambda: daljinskiPritisnut())
        self.pushButton.clicked.connect(self.changeToPrintUi)

    def changeToPrintUi(self):
        widget.setCurrentWidget(PrintUi)


class PrintUi(QMainWindow):
    def __init__(self):
        super(PrintUi, self).__init__()
        uic.loadUi("res/ui/print.ui", self)
        self.pushButton.clicked.connect(self.printPressed)

    def printPressed(self):
        im1 = Image.open('res/session/gotovaKartica.png')

        def get_concat_h(im1):
            dst = Image.new('RGB', (im1.width + im1.width + 35, im1.height))
            dst.paste(im1, (35, 0))
            dst.paste(im1, (im1.width + 35, 0))
            return dst

        get_concat_h(im1).save('res/session/dupla_kartica.png')


        conn.printFile(PrinterUsing, "res/session/dupla_kartica.png", "title", emptyDict)

        widget.setCurrentWidget(AlbumUi)


class AlbumUi(QMainWindow):
    def __init__(self):
        super(AlbumUi, self).__init__()
        uic.loadUi("res/ui/album.ui", self)

        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio1"))
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio3"))

        print(self.buttonGroup.checkedButton())

        self.pushButton.clicked.connect(self.sharePressed)

    def sharePressed(self):

        if self.buttonGroup.checkedId() == -2:
            upload("res/session/slika1.jpg",
                   public_id="djenka/saraiantonio2904/album/" + str(time.time()))
        elif self.buttonGroup.checkedId() == -3:
            upload("res/session/slika2.jpg",
                   public_id="djenka/saraiantonio2904/album/" + str(time.time()))
        elif self.buttonGroup.checkedId() == -4:
            upload("res/session/slika3.jpg",
                   public_id="djenka/saraiantonio2904/album/" + str(time.time()))
        else:
            print("No radio button is selected")
            print(self.buttonGroup.checkedId())

        widget.setCurrentWidget(SplashUi)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

SplashUi = SplashUi()
widget.addWidget(SplashUi)

CameraUi = CameraUi()
widget.addWidget(CameraUi)

PrintUi = PrintUi()
widget.addWidget(PrintUi)

AlbumUi = AlbumUi()
widget.addWidget(AlbumUi)

widget.showFullScreen()
app.exec_()
