from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import sys
import keyboard
import res
from functions import uploadToAlbum, printaj, napraviQr
import json
import subprocess

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']

# konvertiranje qrc u py
qrc_file = 'res/ui/'+tema+'/res.qrc'
pyres_file = 'res.py'
subprocess.run(['pyrcc5', qrc_file, '-o', pyres_file])

# napravi qr kod
napraviQr(eventId)


class SplashUi(QMainWindow):
    def __init__(self):
        super(SplashUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/splash.ui", self)

        # qr kod
        self.qr = self.findChild(QtWidgets.QLabel, 'qr')
        qrPixmap = QPixmap(
            'res/event/' + eventId + '/qr.png')
        self.qr.setPixmap(qrPixmap)
        # link
        self.link = self.findChild(QtWidgets.QLabel, 'link')
        self.link.setText("djenka.tk/"+eventId)

        self.pushButton.clicked.connect(self.changeToCameraUi)

    def changeToCameraUi(self):

        widget.setCurrentWidget(CameraUi)


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

        def daljinskiPritisnut():
            print("k was pressed")

        keyboard.add_hotkey('k', lambda: daljinskiPritisnut())
        self.pushButton.clicked.connect(self.changeToPrintUi)

    def changeToPrintUi(self):
        widget.setCurrentWidget(PrintUi)


class PrintUi(QMainWindow):
    def __init__(self):
        super(PrintUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/print.ui", self)

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
        img1pixmap = QPixmap('res/session/slika1.jpg')
        img2pixmap = QPixmap('res/session/slika2.jpg')
        img3pixmap = QPixmap('res/session/slika3.jpg')
        self.img1.setPixmap(img1pixmap)
        self.img2.setPixmap(img2pixmap)
        self.img3.setPixmap(img3pixmap)
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

    def sharePressed(self):
        # provjerava koji je radiobutton ukljucen
        if self.buttonGroup.checkedId() == -2:
            brojSlike = 1
        elif self.buttonGroup.checkedId() == -3:
            brojSlike = 2
        elif self.buttonGroup.checkedId() == -4:
            brojSlike = 3
        else:
            print("No radio button is selected")

        uploadToAlbum(brojSlike, eventId)

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
