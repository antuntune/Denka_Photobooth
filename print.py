from PyQt5.QtWidgets import QMainWindow, QLabel, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PIL import Image
import json
import cups
import os
import time


# spajanje na cups
conn = cups.Connection()
printers = conn.getPrinters()
# printers is a dictionary containing information about all the printers available

emptyDict = {}
AvailablePrinters = list(printers.keys())
PrinterUsing = AvailablePrinters[0]

class TimeOutThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        time.sleep(60)  # Timeout for splash screen
        self.finished.emit()  # Emit the 'finished' signal when the work is done


class PrintUi(QMainWindow):
    def __init__(self):
        super(PrintUi, self).__init__()

        self.loaded_resources = False
        self.skipButtonPressed = False

        self.timeout_thread = TimeOutThread(parent=self)
        self.timeout_thread.finished.connect(self.timeoutThreadFinished)

    def timeoutThreadFinished(self):
        if self.skipButtonPressed == False:
            self.parent().setCurrentIndex(1)

    def loadResources(self):
        uic.loadUi(os.getcwd() + "/res/ui/"+self.tema+"/print.ui", self)

        self.strip1 = self.findChild(QLabel, 'strip1')
        self.strip2 = self.findChild(QLabel, 'strip2')
        self.strip3 = self.findChild(QLabel, 'strip3')
        self.strip4 = self.findChild(QLabel, 'strip4')
        self.strip5 = self.findChild(QLabel, 'strip5')
        self.strip6 = self.findChild(QLabel, 'strip6')

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio4"))

        # Button sound effect
        self.btn_sfx = QSoundEffect()
        self.btn_sfx.setSource(QUrl.fromLocalFile(os.getcwd() + 'res/ui/btn.wav'))
        self.pushButton.pressed.connect(self.btn_sfx.play)

        self.pushButton.clicked.connect(self.printPressed)
        self.skipButton.clicked.connect(self.skipPressed)


        

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

    def showEvent(self, a0: QShowEvent) -> None:

        if not self.loaded_resources:
            self.loadFromJson()
            self.loadResources()
            self.loaded_resources = True

        stripPixmap = QPixmap(self.eventAlbumPath + self.eventId + "finished" + ".jpg")

        self.strip1.setPixmap(stripPixmap)
        self.strip2.setPixmap(stripPixmap)
        self.strip3.setPixmap(stripPixmap)
        self.strip4.setPixmap(stripPixmap)
        self.strip5.setPixmap(stripPixmap)
        self.strip6.setPixmap(stripPixmap)

        self.skipButtonPressed = False
        self.timeout_thread.start()

        return super().showEvent(a0)

    def printPressed(self):

        if self.buttonGroup.checkedId() == -2:
            kolKartica = 2
        elif self.buttonGroup.checkedId() == -3:
            kolKartica = 4
        else:
            print("No radio button is selected")

        self.printaj(kolKartica)

        self.parent().setCurrentIndex(1)


    def skipPressed(self):
        self.skipButtonPressed = True
        self.parent().setCurrentIndex(1)

    def printaj(self, kolKartica):
        self.skipButtonPressed = True

        im1 = Image.open(self.eventAlbumPath + self.eventId + "finished" + ".jpg")

        def get_concat_h(im1):
            dst = Image.new('RGB', (im1.width + im1.width + 35, im1.height))
            dst.paste(im1, (35, 0))
            dst.paste(im1, (im1.width + 35, 0))
            return dst

        get_concat_h(im1).save(self.eventAlbumPath + self.eventId + "double" + ".jpg", quality=96)

        conn.printFile(
            PrinterUsing, self.eventAlbumPath + self.eventId + "double" + ".jpg", "title", emptyDict)
        print('printam dve kartice')

        if kolKartica == 4:
            conn.printFile(
                PrinterUsing, self.eventAlbumPath + self.eventId + "double" + ".jpg", "title", emptyDict)
            print('printam JOS dve kartice')
