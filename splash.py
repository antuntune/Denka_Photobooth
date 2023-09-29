from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QAction
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, Qt, pyqtSlot, QEvent, QTimer
from PyQt5.QtMultimedia import QSoundEffect
import json
import os, time
import importlib
import pyautogui, threading

from PyQt5.QtGui import QCursor  # Add this import



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

                # Detect the toolbar area
        self.parent.detect_toolbar_area()
        #self.toolbar.addAction(action1)
        #self.parent.mouse_thread.start()
        



        QApplication.processEvents()
        #self.finished.emit()  # Emit the 'finished' signal when the work is done


class SplashUi(QMainWindow):
    def __init__(self):
        super(SplashUi, self).__init__()

        self.loaded_resources = False
        self.load_thread = LoadingThread(parent=self)
        #self.load_thread.finished.connect(self.loading_thread_finished)

        # Set up variables
        self.mouse_moving = False
        self.toolbar_visible = False

        # Detect the toolbar area
        #self.detect_toolbar_area()

        # Create a QTimer to check mouse movement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_mouse_movement)
        


    
    def detect_toolbar_area(self):
        # Get the position and dimensions of the toolbar
        self.toolbar_geometry = self.toolbar.geometry()
        
        # Extract the toolbar area coordinates (x1, y1, x2, y2)
        self.toolbar_area = (
            self.toolbar_geometry.left(),
            self.toolbar_geometry.top(),
            self.toolbar_geometry.right(),
            self.toolbar_geometry.bottom()
        )
        print(self.toolbar_area)



    def check_mouse_movement(self):
        # Get the cursor position
        cursor_pos = QCursor.pos()
        cursor_x, cursor_y = cursor_pos.x(), cursor_pos.y()

        # Check if the cursor is within the toolbar area
        if (self.toolbar_area[0] <= cursor_x <= self.toolbar_area[2] and
                self.toolbar_area[1] <= cursor_y <= self.toolbar_area[3]):
            if not self.toolbar_visible:
                print("Show toolbar (implement your code here)")
                self.toolbar.setHidden(False)
                self.toolbar_visible = True
        else:
            if self.toolbar_visible:
                print("Hide toolbar (implement your code here)")
                self.toolbar.setHidden(True)
                self.toolbar_visible = False



    def settings(self):
        # Back to the config screen
        self.parent().setCurrentIndex(0)


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

        self.actionSettings.triggered.connect(self.settings)
        self.toolbar.setHidden(True)
        self.timer.start(1000)  # Check every second

        QApplication.processEvents()
        return super().showEvent(event)
        

    def buttonPressed(self):

        self.pushButton.hide()
        QApplication.processEvents()
        self.parent().setCurrentIndex(2)
