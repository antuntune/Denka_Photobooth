from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtMultimedia import QSoundEffect
import os
import importlib


class SplashUi(QMainWindow):
    def __init__(self):
        super(SplashUi, self).__init__()

        self.loaded_resources = False

    def showEvent(self, event):

        if not self.loaded_resources:
            uic.loadUi(os.getcwd() + "/res/ui/"+"denka"+"/splash.ui", self)
            # Button sound effect
            self.btn_sfx = QSoundEffect()
            self.btn_sfx.setSource(QUrl.fromLocalFile(os.getcwd() + '/res/ui/btn.wav'))
            self.startButton.pressed.connect(self.btn_sfx.play)
            self.startButton.clicked.connect(self.startButtonPressed)
            self.configScreenButton.clicked.connect(self.return_to_conf)
            self.loaded_resources = True

        self.startButton.show()

        #QApplication.processEvents()
        return super().showEvent(event)
        

    def startButtonPressed(self):
        self.startButton.hide()
        QApplication.processEvents()
        self.parent().setCurrentIndex(2)

    def return_to_conf(self):
        self.parent().setCurrentIndex(0)
