from PyQt5.QtWidgets import QMainWindow, QLabel, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PIL import Image
import json
import cups

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']

# spajanje na cups
conn = cups.Connection()
printers = conn.getPrinters()
# printers is a dictionary containing information about all the printers available

emptyDict = {}
AvailablePrinters = list(printers.keys())
PrinterUsing = AvailablePrinters[0]


class PrintUi(QMainWindow):
    def __init__(self):
        super(PrintUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/print.ui", self)

        self.strip1 = self.findChild(QLabel, 'strip1')
        self.strip2 = self.findChild(QLabel, 'strip2')
        self.strip3 = self.findChild(QLabel, 'strip3')
        self.strip4 = self.findChild(QLabel, 'strip4')
        self.strip5 = self.findChild(QLabel, 'strip5')
        self.strip6 = self.findChild(QLabel, 'strip6')

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio4"))

        self.pushButton.clicked.connect(self.printPressed)
        self.skipButton.clicked.connect(self.skipPressed)

    def showEvent(self, a0: QShowEvent) -> None:

        stripPixmap = QPixmap('res/session/gotovaKartica.png')

        self.strip1.setPixmap(stripPixmap)
        self.strip2.setPixmap(stripPixmap)
        self.strip3.setPixmap(stripPixmap)
        self.strip4.setPixmap(stripPixmap)
        self.strip5.setPixmap(stripPixmap)
        self.strip6.setPixmap(stripPixmap)

        return super().showEvent(a0)

    def printPressed(self):

        if self.buttonGroup.checkedId() == -2:
            kolKartica = 2
        elif self.buttonGroup.checkedId() == -3:
            kolKartica = 4
        else:
            print("No radio button is selected")

        self.printaj(kolKartica)

        self.parent().setCurrentIndex(4)

    def skipPressed(self):
        self.parent().setCurrentIndex(4)

    def printaj(self, kolKartica):
        im1 = Image.open('res/session/gotovaKartica.png')

        def get_concat_h(im1):
            dst = Image.new('RGB', (im1.width + im1.width + 35, im1.height))
            dst.paste(im1, (35, 0))
            dst.paste(im1, (im1.width + 35, 0))
            return dst

        get_concat_h(im1).save('res/session/dupla_kartica.png')

        conn.printFile(
            PrinterUsing, "res/session/dupla_kartica.png", "title", emptyDict)
        print('printam dve kartice')

        if kolKartica == 4:
            conn.printFile(
                PrinterUsing, "res/session/dupla_kartica.png", "title", emptyDict)
            print('printam JOS dve kartice')
