from PyQt5.QtWidgets import QMainWindow, QComboBox
from PyQt5 import uic
import qrcode
import json
import subprocess
import os
import shutil



class ConfigUi(QMainWindow):
    def __init__(self):
        #self.ID = eventId[0]

        super(ConfigUi, self).__init__()
        uic.loadUi("res/ui/config.ui", self)
        self.initJsonVar()
        self.combobox = self.findChild(QComboBox, 'comboBox')
        self.combobox.addItems(self.eventId_)
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.onComboBoxIndexChanged)
        self.pushButton.clicked.connect(self.buttonPressed)

  

    def initJsonVar(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('config.json', 'r') as f:
            # Load the contents of the file into a dictionary
            config = json.load(f)
            self.eventId_ = config['eventId_']
            self.tema_ = config['tema_']

        self.eventId = self.eventId_[0]
        self.tema = self.tema_[0]
        self.albumPath = os.path.expanduser("~") + "/EventAlbums/"

    def onComboBoxIndexChanged(self, index):
        # update selected event to variable
        self.eventId = self.combobox.currentText()

    def loadJson(self):
        self.eventAlbumPath = self.albumPath + self.eventId + "/"
        self.cardPath = self.eventAlbumPath + "/" + self.eventId + ".jpg"
        # Create a dictionary with the specific key-value pair
        data = {
            "eventId_": self.eventId_,
            "tema_": self.tema_,
            "eventId": self.eventId,
            "tema": self.tema,
            "albumPath": self.albumPath,
            "eventAlbumPath": self.eventAlbumPath,
            "cardPath": self.cardPath
        }

        # Write data to the JSON file
        with open("config.json", "w") as file:
            json.dump(data, file)

    def runSh(self):

        script_path = os.getcwd() + "/modprobe.sh"
        subprocess.run(['sh', script_path], check=True)


    def buttonPressed(self):
        self.loadJson()
        self.createEventMap()
        self.napraviQr()
        self.copyEventCard()
        self.runSh()
        self.parent().setCurrentIndex(1)

    def napraviQr(self):
        img = qrcode.make('www.denka.live/' + self.eventId)
        type(img)  # qrcode.image.pil.PilImage
        img.save(self.albumPath + self.eventId + "/qr.png")

    def createEventMap(self):
        # root mapa albuma
        directory = self.albumPath
        if not os.path.exists(directory):
            os.makedirs(directory)

        # kreiraj mapu događaja ako je jos nema
        directory = self.albumPath + self.eventId
        if not os.path.exists(directory):
            os.makedirs(directory)

        # unutar mape događaja kreiraj mapu za slike
        directory = self.albumPath + self.eventId + "/picAlbum"
        if not os.path.exists(directory):
            os.makedirs(directory)

    def copyEventCard(self):
        # kopiraj karticu dogadaja u mapu dogadaja
        shutil.copy2(os.getcwd() +"/res/cardPool/" + self.eventId + ".jpg", self.albumPath + self.eventId)
