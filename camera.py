from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtMultimedia import QSoundEffect
from PIL import Image, ImageOps, ImageEnhance
import threading
import cv2
from time import sleep
from datetime import datetime
from video_stream import VideoThread
import dslr
import shutil, os, signal
import time
import importlib
import json


class WorkerThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # Access objects and data from the parent (MainWindow) class
        # using self.parent
        # Example: Accessing an object and calling its method
        #self.parent.some_object.some_method()
        self.parent.slikanje()
        self.finished.emit()  # Emit the 'finished' signal when the work is done


class CameraUi(QMainWindow):
    def __init__(self):
        super(CameraUi, self).__init__()

        self.loaded_resources = False
        self.count = 1
        self.flag = 0

        self.worker_thread = WorkerThread(parent=self)
        self.worker_thread.finished.connect(self.threadFinished)

        self.movie = QMovie(os.getcwd() + "/res/ui/5sec.gif")

        self.videoLoading = QMovie(os.getcwd() + "/res/ui/videoLoading.gif")

        self.camera_thread = VideoThread()
        self.camera_thread.frameCaptured.connect(self.updateFrame)


    def loadResources(self):

        uic.loadUi(os.getcwd() + "/res/ui/"+self.tema+"/camera.ui", self)

        self.strip = self.findChild(QtWidgets.QLabel, 'strip')
        stripPixmap = QPixmap(self.cardPath)
        self.strip.setPixmap(stripPixmap)

        self.cardSlot1 = self.findChild(QtWidgets.QLabel, 'img1')
        self.cardSlot2 = self.findChild(QtWidgets.QLabel, 'img2')
        self.cardSlot3 = self.findChild(QtWidgets.QLabel, 'img3')
        self.streamLabel = self.findChild(QtWidgets.QLabel, 'stream')

        # camera sound effect
        #self.btn_sfx = QSoundEffect()
        #self.btn_sfx.setSource(QUrl.fromLocalFile('res/ui/cam.wav'))

        # Create a QLabel widget to display the transparent gif
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        #self.gif_label.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.gif_label.setFixedSize(834, 790)
        self.gif_label.move(400, 200)

        # Create a QMovie object from the gif file
        
        self.gif_label.setMovie(self.movie)
        self.movie.finished.connect(self.countdownFinished)

        self.videoLabel.setMovie(self.videoLoading)
        

        gledaj = QPixmap(os.getcwd() + "/res/ui/"+self.tema+"/gledajteukameru.png")
        self.fullscreenlabel.setPixmap(gledaj)
        self.fullscreenlabel.setVisible(False)
        QApplication.processEvents()


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
            self.cardBright = config['cardBright']

    def showStream(self):
        self.videoLabel.hide()
        self.gif_label.show()
        self.gif_label.raise_()
        self.camera_thread.run()
        QApplication.processEvents()
        

    def updateFrame(self, pixmap):
        self.streamLabel.setPixmap(pixmap)

    def napraviKarticu(self):

        kartica = Image.open(self.cardPath)
        im1 = Image.open(self.eventAlbumPath + "/slika1.jpg").resize((892, 596))
        im2 = Image.open(self.eventAlbumPath + "/slika2.jpg").resize((892, 596))
        im3 = Image.open(self.eventAlbumPath + "/slika3.jpg").resize((892, 596))

        kartica.paste(im1, (54, 217))
        kartica.paste(im2, (54, 879))
        kartica.paste(im3, (54, 1541))

        # Promijeni svijetlinu kartice
        enhancer = ImageEnhance.Brightness(kartica)
        kartica = enhancer.enhance(int(self.cardBright)/100)
        kartica.save(self.eventAlbumPath + self.eventId + "finished" + ".jpg", quality=96)

    # kad se prikaze ekran
    def showEvent(self, event):


        if not self.loaded_resources:
            self.loadFromJson()
            self.loadResources()
            self.loaded_resources = True

        self.videoLabel.show()
        self.videoLoading.start()
        QApplication.processEvents()

        self.count = 1

        # pokreni strim
        self.camera_thread.start()

        self.loadingThread = threading.Timer(3, self.showStream)
        self.loadingThread.start()
        
        # resetiranje pixmapa
        transPixmap = QPixmap(os.getcwd() + "/res/ui/"+self.tema+"/transparent.png")
        self.cardSlot1.setPixmap(transPixmap)
        self.cardSlot2.setPixmap(transPixmap)
        self.cardSlot3.setPixmap(transPixmap)
        # Start the movie
        self.movie.start()
        self.gif_label.hide()
        # tu se tek pojavljuje ekran
        return super().showEvent(event)

    def countdownFinished(self):
        # pokazi gledaj u kameru sliku
        self.fullscreenlabel.setVisible(True)
        self.fullscreenlabel.raise_()
        QApplication.processEvents()
        self.worker_thread.start()

    def threadFinished(self):
        self.fullscreenlabel.setVisible(False)
        QApplication.processEvents()
        if self.flag == 1:
            self.movie.start()
            self.gif_label.hide()
        self.flag = 0
        if self.count == 4:
            self.parent().setCurrentIndex(3)
        

    def slikanje(self):
        # zaustavi stream
        self.camera_thread.stop()
        # okini sliku
        dslr.captureImage()

        if self.count == 1 or self.count == 2:
            self.camera_thread.start()
            self.loadingThread1 = threading.Timer(3, self.showStream)
            self.loadingThread1.start()
            self.videoLabel.show()
            self.videoLoading.start()
            QApplication.processEvents()

            # indikator za sljedeci krug slikanja
            self.flag = 1

        # timestamp
        shot_time = datetime.now().strftime("_%d-%m-%Y_%H:%M:%S")

        # slika (1/2/3) zbog pozicioniranja na karticu
        slika = "slika" + str(self.count)
        # priprema slike za karticu
        dslr.renameImage(slika)

        shutil.copy2(os.getcwd()+ "/" + slika + ".jpg", self.eventAlbumPath + "picAlbum/" + slika + shot_time + ".jpg")

        dslr.resizeImage(slika + ".jpg")
        # premjestanje u mapu dogadaja
        shutil.move(os.getcwd()+ "/" + slika + ".jpg", self.eventAlbumPath + slika + ".jpg")
        QCoreApplication.processEvents()
        
        if self.count == 1:
            img1pixmap = QPixmap(self.eventAlbumPath + slika + ".jpg")
            self.cardSlot1.setPixmap(img1pixmap)
            
        elif self.count == 2:
            img2pixmap = QPixmap(self.eventAlbumPath + slika + ".jpg")
            self.cardSlot2.setPixmap(img2pixmap)

        elif self.count == 3:
            img3pixmap = QPixmap(self.eventAlbumPath + slika + ".jpg")
            self.cardSlot3.setPixmap(img3pixmap)
            # zavrsi slikanje, pravi karticu i prebac ekran
            #self.movie.finished.disconnect(self.slikaj)
            self.napraviKarticu()


        # Increment count
        self.count += 1

        
        
