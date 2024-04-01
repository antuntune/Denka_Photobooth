from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QAction
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, Qt, pyqtSlot, QEvent, QTimer
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QMainWindow, QToolBar
from PyQt5.QtCore import QPoint, QTimer, QSize
from PyQt5.QtGui import QIcon
import json
import os, time
import importlib
import pyautogui, threading
import random
from share_server import update_predefined_text

from PyQt5.QtGui import QCursor  # Add this import


class MouseMoveThread(QThread):
    mouseMoved = pyqtSignal(QPoint)  # Signal emitted when mouse moves

    def run(self):
        prev_pos = None
        while True:
            current_pos = QCursor.pos()
            if current_pos != prev_pos:
                prev_pos = current_pos
                self.mouseMoved.emit(current_pos)
            time.sleep(0.05)  # Adjust sleep time as needed


class LoadingThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # qr kod
        #self.parent.qr = self.parent.findChild(QLabel, 'qr')
        #qrPixmap = QPixmap(self.parent.eventAlbumPath + '/qr.png')
        #self.parent.qr.setPixmap(qrPixmap)
        #self.parent.qr.show()
        # link
        #self.parent.link = self.parent.findChild(QLabel, 'link')
        #print("www.denka.live/"+self.parent.eventId)
        #self.parent.link.setText("www.denka.live/"+self.parent.eventId)
        #self.parent.link.show()
        pass
        #QApplication.processEvents()


class SplashUi(QMainWindow):
    def __init__(self):
        super(SplashUi, self).__init__()

        self.loaded_resources = False
        self.load_thread = LoadingThread(parent=self)

    def return_to_conf(self):
        self.parent().setCurrentIndex(0)


    def loadFromJson(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('config.json', 'r') as f:
            # Load the contents of the file into a dictionary
            config = json.load(f)
            self.eventId = config['eventId']
            self.tema = config['tema']
            self.eventAlbumPath = config['eventAlbumPath']


    def mouseMoved(self, pos):
        # Handle mouse movement
        toolbar_rect = self.toolbar.geometry()
        toolbar_global_pos = self.toolbar.mapToGlobal(QPoint(0, 0))
        if toolbar_rect.contains(pos - toolbar_global_pos):
            self.toolbar.show()
            self.timer.stop()  # Stop the timer
        else:
            if not self.timer.isActive():
                self.timer.start(500)  # Start the timer with a delay of 500 milliseconds


    def hideToolbar(self):
        self.toolbar.hide()

    def readPIN(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('pin.json', 'r') as f:
            # Load the contents of the file into a dictionary
            pin = json.load(f)
        self.lastSessionPin = pin['PIN']

    def loadPIN(self):
        self.readPIN()
        self.sessionPin = random.randint(1000, 9999)
        pin = {
            "PIN": self.sessionPin,
            "lastPin": self.lastSessionPin
        }
        print("Splash actual PIN ", self.sessionPin)
        #print("Splash last PIN ", self.self.lastSessionPin)
        # Write data to the JSON file
        with open("pin.json", "w") as file:
            json.dump(pin, file)
        update_predefined_text(self.sessionPin, self.lastSessionPin)


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

        # Create a toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.hide()  # Hide the toolbar initially

        # Set the icon size for toolbar buttons
        icon_size = QSize(64, 64)  # Width, Height
        self.toolbar.setIconSize(icon_size)

        # Create actions for the toolbar
        self.conf = QAction(QIcon(os.getcwd() + "/res/ui/"+self.tema+"/config.png"), "Configuration", self)
        # Add actions to the toolbar
        self.toolbar.addAction(self.conf)
        self.conf.triggered.connect(self.return_to_conf)

        # Track mouse movement in a separate thread
        self.mouse_thread = MouseMoveThread()
        self.mouse_thread.mouseMoved.connect(self.mouseMoved)
        self.mouse_thread.start()

        # Timer for delayed hiding of toolbar
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hideToolbar)

        self.loadPIN()

        self.pushButton.show()

        QApplication.processEvents()
        return super().showEvent(event)
        

    def buttonPressed(self):
        # Thread for building WhatsApp qr code for contact
        thread = threading.Thread(target=self.buildWappQr)
        # Start the thread
        thread.start()

        self.pushButton.hide()
        QApplication.processEvents()
        self.parent().setCurrentIndex(2)

    def buildWappQr(self):
        # Create Qr code for WhatsApp contact
        #createWappQr()
        pass