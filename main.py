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
import keyboard


import res

from functions import uploadToAlbum, printaj


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

        self.strip = self.findChild(QtWidgets.QLabel, 'strip')
        stripPixmap = QPixmap('res/event/kartica.png')
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

        self.strip1 = self.findChild(QtWidgets.QLabel, 'strip1')
        self.strip2 = self.findChild(QtWidgets.QLabel, 'strip2')
        self.strip3 = self.findChild(QtWidgets.QLabel, 'strip3')
        self.strip4 = self.findChild(QtWidgets.QLabel, 'strip4')
        self.strip5 = self.findChild(QtWidgets.QLabel, 'strip5')
        self.strip6 = self.findChild(QtWidgets.QLabel, 'strip6')

        stripPixmap = QPixmap('res/session/gotovaKartica.png')

        self.strip1.setPixmap(stripPixmap)
        self.strip2.setPixmap(stripPixmap)
        self.strip3.setPixmap(stripPixmap)
        self.strip4.setPixmap(stripPixmap)
        self.strip5.setPixmap(stripPixmap)
        self.strip6.setPixmap(stripPixmap)

        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio4"))

        self.pushButton.clicked.connect(self.printPressed)

    def printPressed(self):

        if self.buttonGroup.checkedId() == -2:
            kolKartica = 2
        elif self.buttonGroup.checkedId() == -3:
            kolKartica = 4
        else:
            print("No radio button is selected")

        printaj(kolKartica)

        widget.setCurrentWidget(AlbumUi)


class AlbumUi(QMainWindow):
    def __init__(self):
        super(AlbumUi, self).__init__()
        uic.loadUi("res/ui/album.ui", self)

        self.img1 = self.findChild(QtWidgets.QLabel, 'img1')
        self.img2 = self.findChild(QtWidgets.QLabel, 'img2')
        self.img3 = self.findChild(QtWidgets.QLabel, 'img3')

        img1pixmap = QPixmap('res/session/slika1.jpg')
        img2pixmap = QPixmap('res/session/slika2.jpg')
        img3pixmap = QPixmap('res/session/slika3.jpg')

        self.img1.setPixmap(img1pixmap)
        self.img2.setPixmap(img2pixmap)
        self.img3.setPixmap(img3pixmap)

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
            brojSlike = 1
        elif self.buttonGroup.checkedId() == -3:
            brojSlike = 2
        elif self.buttonGroup.checkedId() == -4:
            brojSlike = 3
        else:
            print("No radio button is selected")

        uploadToAlbum(brojSlike)

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
