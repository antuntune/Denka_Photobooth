from PyQt5.QtWidgets import QMainWindow, QComboBox
from PyQt5 import uic
import qrcode
import json
import subprocess

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
    eventId = config['eventId']

# mongodb spajanje
# client = pymongo.MongoClient(
#     "mongodb+srv://antuntun:yF0vqRb8HdxMdAKJ@cluster0.io95d.mongodb.net/?retryWrites=true&w=majority")
# db = client['DenkaPhotobooth']
# collection = db['events']

# field = 'name'

# items = collection.distinct(field)

items = ['Sara i Antonio']


class ConfigUi(QMainWindow):
    def __init__(self):
        super(ConfigUi, self).__init__()
        uic.loadUi("res/ui/config.ui", self)

        self.combobox = self.findChild(QComboBox, 'comboBox')

        self.combobox.addItems(items)

        self.combobox.setCurrentIndex(0)

        self.pushButton.clicked.connect(self.buttonPressed)

    def buttonPressed(self):

        #subprocess.Popen('modprobe v4l2loopback', shell=True)
        #subprocess.Popen('snap connect ffmpeg:camera', shell=True)


        self.parent().setCurrentIndex(1)
        self.napraviQr(eventId)

    def napraviQr(self, eventId):
        img = qrcode.make('www.denka.live/' + eventId)
        type(img)  # qrcode.image.pil.PilImage
        img.save("res/event/" + eventId + "/qr.png")
