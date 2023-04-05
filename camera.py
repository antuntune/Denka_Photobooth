from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
import json
from PIL import Image, ImageOps, Image
import threading
import cv2
from pynput import keyboard
from time import sleep
from datetime import datetime
from video_stream import VideoThread
import dslr
import shutil, os, signal

sessionPath = "/home/marko/Documents/backup_2/Denka_Photobooth/"


# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
    eventId = config['eventId']
    tema = config['tema']
    mode = config['mode']

src_path = '/path/to/source/file.jpg'
dest_path = '/path/to/destination/'

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

        # camera sound effect
        self.btn_sfx = QSoundEffect()
        self.btn_sfx.setSource(QUrl.fromLocalFile('res/ui/cam.wav'))

        # Create a QLabel widget to display the transparent gif
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.gif_label.setFixedSize(834, 790)

        self.gif_label.move(400, 200)

        # Create a QMovie object from the gif file
        self.movie = QMovie("res/ui/5sec.gif")
        self.gif_label.setMovie(self.movie)

        self.camera_thread_1 = VideoThread()
        self.camera_thread_1.frameCaptured.connect(self.updateFrame)

        self.camera_thread_2 = VideoThread()
        self.camera_thread_2.frameCaptured.connect(self.updateFrame)

        self.camera_thread_3 = VideoThread()
        self.camera_thread_3.frameCaptured.connect(self.updateFrame)

    def updateFrame(self, pixmap):
        self.streamLabel.setPixmap(pixmap)

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

        # pokreni strim
        self.camera_thread_1.start()
        self.mode = mode
        self.count = 1
        # resetiranje pixmapa
        transPixmap = QPixmap("res/ui/"+tema+"/transparent.png")
        self.cardSlot1.setPixmap(transPixmap)
        self.cardSlot2.setPixmap(transPixmap)
        self.cardSlot3.setPixmap(transPixmap)

        if self.mode == "odbr":
            self.movie.finished.connect(self.slikaj)
            # Start the movie
            self.movie.start()
        else:
            # ZA TASTATURU
            def on_press(key):
                if key.char == 'k':
                    self.slikaj()
            def listener_thread():
                with keyboard.Listener(on_press=on_press) as self.listener:
                    self.listener.join()
            self.listener = threading.Thread(target=listener_thread)
            self.listener.start()

        # tu se tek pojavljuje ekran
        return super().showEvent(a0)

    def captureImageThread(self):
        dslr.killGphoto2Process()
        dslr.captureImage()


    def slikaj(self):
        # Stop the camera capture thread
        dslr.killStream()
        if self.count==1:
            self.camera_thread_1.stop() 
            self.camera_thread_1.quit()

        if self.count==2:
            self.camera_thread_2.stop() 
            self.camera_thread_2.quit()

        if self.count==3:
            self.camera_thread_3.stop() 
            self.camera_thread_3.quit()

        t = threading.Thread(target=self.captureImageThread)
        t.start()
        t.join()

        # timestamp
        shot_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        # prikaz slike na karticu
        if self.count == 1:
            # pokreni stream
            self.camera_thread_2.start()

            dslr.renameImage("slika1")
            # resajzaj sliku
            dslr.resizeImage("slika1.jpg")
            # ne radi lodanje slike u label poslje slikanja
            pixmap = QPixmap('slika1.jpg')
            self.streamLabel.setPixmap(pixmap)
            self.streamLabel.show()
            new_filename = "slika1" + shot_time +".jpg"
            shutil.copy("slika1.jpg", new_filename)
            shutil.copy2(sessionPath + "slika1.jpg", sessionPath + "/res/session/")
            shutil.move(sessionPath + new_filename, sessionPath +  "/res/event/sia2904_session")
            os.remove(sessionPath + "/slika1.jpg")
            img1pixmap = QPixmap('res/session/slika1.jpg')
            self.cardSlot1.setPixmap(img1pixmap)

        elif self.count == 2:
            # pokreni stream
            self.camera_thread_3.start()
            
            dslr.renameImage("slika2")
            dslr.resizeImage("slika2.jpg")
            new_filename = "slika2" + shot_time +".jpg"
            shutil.copy("slika2.jpg", new_filename)
            shutil.copy2(sessionPath + "slika2.jpg", sessionPath + "/res/session/")
            shutil.move(sessionPath + new_filename, sessionPath +  "/res/event/sia2904_session")
            os.remove(sessionPath + "/slika2.jpg")
            img1pixmap = QPixmap('res/session/slika2.jpg')
            img2pixmap = QPixmap('res/session/slika2.jpg')
            self.cardSlot2.setPixmap(img2pixmap)

        elif self.count == 3:
            dslr.renameImage("slika3")
            dslr.resizeImage("slika3.jpg")
            new_filename = "slika3" + shot_time +".jpg"
            shutil.copy("slika3.jpg", new_filename)
            shutil.copy2(sessionPath + "slika3.jpg", sessionPath + "/res/session/")
            shutil.move(sessionPath + new_filename, sessionPath +  "/res/event/sia2904_session")
            os.remove(sessionPath + "/slika3.jpg")
            img1pixmap = QPixmap('res/session/slika3.jpg')
            img3pixmap = QPixmap('res/session/slika3.jpg')
            self.cardSlot3.setPixmap(img3pixmap)

        
        # Increment count
        self.count += 1
        # Nakon zadnje slike
        if self.count > 3:
            if self.mode == 'odbr':
                self.movie.finished.disconnect(self.slikaj)
            else:
                self.listener.stop()
            self.napraviKarticu(eventId)
            self.changeToPrintUi()
        else:
            if self.mode == 'odbr':
                self.movie.start()



