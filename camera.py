
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import json
from PIL import Image

import cv2
import os
import keyboard
import queue

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
        self.streamLabel = self.findChild(QtWidgets.QLabel, 'stream')

    def update_image(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        qImg = QImage(rgb_frame.data, w, h, ch*w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.streamLabel.setPixmap(pixmap.scaled(
            self.streamLabel.size(), Qt.KeepAspectRatio))

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

    # kad se prikaze ekran
    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.count = 1

        # resetiranje pixmapa
        transPixmap = QPixmap("res/ui/"+tema+"/transparent.png")
        self.cardSlot1.setPixmap(transPixmap)
        self.cardSlot2.setPixmap(transPixmap)
        self.cardSlot3.setPixmap(transPixmap)

        # pokreni strim
        self.thread = CameraThread()
        self.thread.image_data.connect(self.update_image)
        self.thread.start()

        keyboard.add_hotkey('k', lambda: self.slikaj())

        # tu se tek pojavljuje ekran
        return super().showEvent(a0)

    def slikaj(self):

        # Stop the camera capture thread
        self.thread.stop()
        # čeka da se thread ugasi pa onda ide dalje
        self.thread.wait()

        # Capture a single frame from the camera
        _, frame = cv2.VideoCapture(0).read()

        # Convert the image to a QImage
        q_image = QImage(
            frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

        # Save image to disk
        filename = f'res/session/slika{self.count}.jpg'
        cv2.imwrite(filename, frame)

        # Print message to console
        print(f'Image {self.count} saved to {filename}')

        # prikaz slike na karticu
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

        # Resume the camera capture thread
        self.thread = CameraThread()
        self.thread.image_data.connect(self.update_image)
        self.thread.start()

        # Nakon zadnje slike
        if self.count > 3:
            keyboard.unhook_all_hotkeys()
            self.napraviKarticu(eventId)
            self.thread.stop()
            self.changeToPrintUi()


class CameraThread(QThread):
    image_data = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.capture = cv2.VideoCapture(0)
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            ret, frame = self.capture.read()

            if ret:
                self.image_data.emit(frame)

        self.capture.release()
