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
import threading
#from cloudinaryUpload import uploadImage


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
        

        self.timeout_thread = TimeOutThread(parent=self)
        self.timeout_thread.finished.connect(self.timeoutThreadFinished)


    def timeoutThreadFinished(self):
        self.parent().setCurrentIndex(1)

    def loadResources(self):
        uic.loadUi(os.getcwd() + "/res/ui/"+self.tema+"/print.ui", self)

        self.strip1 = self.findChild(QLabel, 'strip1')
        self.strip2 = self.findChild(QLabel, 'strip2')
        self.strip3 = self.findChild(QLabel, 'strip3')
        self.strip4 = self.findChild(QLabel, 'strip4')
        self.strip5 = self.findChild(QLabel, 'strip5')
        self.strip6 = self.findChild(QLabel, 'strip6')
        self.strip7 = self.findChild(QLabel, 'strip7')
        self.strip8 = self.findChild(QLabel, 'strip8')



        # Button sound effect
        self.btn_sfx = QSoundEffect()
        self.btn_sfx.setSource(QUrl.fromLocalFile(os.getcwd() + 'res/ui/btn.wav'))
        self.pushButton.pressed.connect(self.btn_sfx.play)

        self.pushButton.clicked.connect(self.printPressed)
        self.skipButton.clicked.connect(self.skipPressed)

        self.plusButton.clicked.connect(self.plus_strip_num)
        self.minusButton.clicked.connect(self.minus_strip_num)

    def plus_strip_num(self):
        # Increment the current image index
        self.current_image_index = (self.current_image_index + 1) % len(self.pixmaps) 
        if self.current_image_index > self.max_pic_num or self.current_image_index == 0:
            self.current_image_index = int(self.max_pic_num)
        # Update the image displayed
        self.update_print_num_image()
        print(self.max_pic_num)

    def minus_strip_num(self):
        # Increment the current image index
        self.current_image_index = (self.current_image_index - 1) % len(self.pixmaps)
        if self.current_image_index == len(self.pixmaps) - 1:
            self.current_image_index = 0
        print(self.current_image_index)
        # Update the image displayed
        self.update_print_num_image()

        

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
            self.print_limit_num = config['print_limit_num']
            self.shareImages = config['shareImages']

    def showEvent(self, a0: QShowEvent) -> None:

        self.loadFromJson()
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
        self.strip7.setPixmap(stripPixmap)
        self.strip8.setPixmap(stripPixmap)

        self.strip1.setVisible(False)
        self.strip2.setVisible(False)
        self.strip3.setVisible(False)
        self.strip4.setVisible(False)
        self.strip5.setVisible(False)
        self.strip6.setVisible(False)
        self.strip7.setVisible(False)
        self.strip8.setVisible(False)


        # Load the QPixmap objects for each image
        self.pixmaps = [
            QPixmap(os.getcwd() + "/res/ui/"+self.tema+ "/print_nums/" + "two.png"),
            QPixmap(os.getcwd() + "/res/ui/"+self.tema+ "/print_nums/" + "four.png"),
            QPixmap(os.getcwd() + "/res/ui/"+self.tema+ "/print_nums/" + "six.png"),
            QPixmap(os.getcwd() + "/res/ui/"+self.tema+ "/print_nums/" + "eight.png")
        ]
        self.current_image_index = 0

        # Set the initial image
        self.update_print_num_image()

        self.max_pic_num = int((self.print_limit_num / 2 ) - 1)


        self.timeout_thread.start()

        return super().showEvent(a0)

    def update_print_num_image(self):
        # Get the current pixmap
        pixmap = self.pixmaps[self.current_image_index]
        # Scale the pixmap to fit the label while maintaining aspect ratio
        pixmap = pixmap.scaled(self.label.size(), aspectRatioMode=True, transformMode=True)
        # Set the scaled pixmap to the QLabel
        self.label.setPixmap(pixmap)
        print(self.current_image_index)

        if int((self.current_image_index + 1)*2) == 2:
            self.strip1.setVisible(True)
            self.strip2.setVisible(True)
            self.strip3.setVisible(False)
            self.strip4.setVisible(False)
            self.strip5.setVisible(False)
            self.strip6.setVisible(False)
            self.strip7.setVisible(False)
            self.strip8.setVisible(False)
        if int((self.current_image_index + 1)*2) == 4:
            self.strip1.setVisible(True)
            self.strip2.setVisible(True)
            self.strip3.setVisible(True)
            self.strip4.setVisible(True)
            self.strip5.setVisible(False)
            self.strip6.setVisible(False)
            self.strip7.setVisible(False)
            self.strip8.setVisible(False)  
        if int((self.current_image_index + 1)*2) == 6:
            self.strip1.setVisible(True)
            self.strip2.setVisible(True)
            self.strip3.setVisible(True)
            self.strip4.setVisible(True)
            self.strip5.setVisible(True)
            self.strip6.setVisible(True)
            self.strip7.setVisible(False)
            self.strip8.setVisible(False)  
        if int((self.current_image_index + 1)*2) == 8:
            self.strip1.setVisible(True)
            self.strip2.setVisible(True)
            self.strip3.setVisible(True)
            self.strip4.setVisible(True)
            self.strip5.setVisible(True)
            self.strip6.setVisible(True)
            self.strip7.setVisible(True)
            self.strip8.setVisible(True)  


    def printPressed(self):

        # kill timeout thread which set up splash window if timeout happend beacuse print button is pressed
        self.timeout_thread.terminate()


        self.printaj()

        if self.shareImages == True:
            self.parent().setCurrentIndex(4)
        else:
            self.parent().setCurrentIndex(5)


    def skipPressed(self):

        # kill timeout thread which set up splash window if timeout happend beacuse skip button is pressed
        self.timeout_thread.terminate()

        if self.shareImages == True:
            self.parent().setCurrentIndex(4)
        else:
            self.parent().setCurrentIndex(5)

    def printaj(self):


        self.kolKartica = int((self.current_image_index +1) * 2)
        print(self.kolKartica)


        im1 = Image.open(self.eventAlbumPath + self.eventId + "finished" + ".jpg")

        def get_concat_h(im1):
            dst = Image.new('RGB', (im1.width + im1.width + 35, im1.height))
            dst.paste(im1, (35, 0))
            dst.paste(im1, (im1.width + 35, 0))
            return dst

        get_concat_h(im1).save(self.eventAlbumPath + self.eventId + "double" + ".jpg", quality=96)

        #self.eventAlbumPath + self.eventId + "double" + ".jpg", "title"


        for _ in range(int(self.kolKartica / 2)):
            conn.printFile(PrinterUsing, self.eventAlbumPath + self.eventId + "double" + ".jpg", "title", emptyDict)