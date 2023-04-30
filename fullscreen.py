from PyQt5.QtWidgets import QMainWindow, QLabel, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
import json
import cloudinary
import time
from cloudinary.uploader import upload

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']



class FullscreenUi(QMainWindow):
    def __init__(self):
        super(FullscreenUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/gledaj.ui", self)


    def showEvent(self, a0: QShowEvent) -> None:

        

        return super().showEvent(a0)

    