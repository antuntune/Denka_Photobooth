from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtMultimedia import QSoundEffect
import json
import os, time
import importlib




class LoadingThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # qr kod
        self.parent.qr = self.parent.findChild(QLabel, 'qr')
        qrPixmap = QPixmap(self.parent.eventAlbumPath + '/qr.png')
        self.parent.qr.setPixmap(qrPixmap)
        self.parent.qr.show()
        # link
        self.parent.link = self.parent.findChild(QLabel, 'link')
        self.parent.link.setText("www.denka.live/"+self.parent.eventId)
        self.parent.link.show()
        QApplication.processEvents()
        #self.finished.emit()  # Emit the 'finished' signal when the work is done


class SplashUi(QMainWindow):
    def __init__(self):
        super(SplashUi, self).__init__()

        self.loaded_resources = False
        self.load_thread = LoadingThread(parent=self)

    def loadFromJson(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('config.json', 'r') as f:
            # Load the contents of the file into a dictionary
            config = json.load(f)
            self.eventId = config['eventId']
            self.tema = config['tema']
            self.eventAlbumPath = config['eventAlbumPath']

    # kad se prikaze ekran
    def showEvent(self, event):

        if not self.loaded_resources:

            self.loadFromJson()

            uic.loadUi(os.getcwd() + "/res/ui/"+self.tema+"/splash.ui", self)
            # Button sound effect
            self.btn_sfx = QSoundEffect()
            self.btn_sfx.setSource(QUrl.fromLocalFile(os.getcwd() + '/res/ui/btn.wav'))
            self.pushButton.pressed.connect(self.btn_sfx.play)
            self.pushButton.clicked.connect(self.buttonPressed)
            self.load_thread.start()
            self.loaded_resources = True

        self.pushButton.show()
        QApplication.processEvents()
        return super().showEvent(event)
        

    def buttonPressed(self):

        self.pushButton.hide()
        QApplication.processEvents()
        self.parent().setCurrentIndex(2)
