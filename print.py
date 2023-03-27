from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from functions import printaj
import json

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']


class PrintUi(QMainWindow):
    def __init__(self):
        super(PrintUi, self).__init__()
        uic.loadUi("res/ui/"+tema+"/print.ui", self)

        self.strip1 = self.findChild(QtWidgets.QLabel, 'strip1')
        self.strip2 = self.findChild(QtWidgets.QLabel, 'strip2')
        self.strip3 = self.findChild(QtWidgets.QLabel, 'strip3')
        self.strip4 = self.findChild(QtWidgets.QLabel, 'strip4')
        self.strip5 = self.findChild(QtWidgets.QLabel, 'strip5')
        self.strip6 = self.findChild(QtWidgets.QLabel, 'strip6')

        stripPixmap = QPixmap('res/session/gotovaKartica.png')

        self.strip1.setPixmap(stripPixmap)
        self.strip2.setPixmap(stripPixmap)
        self.strip3.setPixmap(stripPixmap)
        self.strip4.setPixmap(stripPixmap)
        self.strip5.setPixmap(stripPixmap)
        self.strip6.setPixmap(stripPixmap)

        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QtWidgets.QRadioButton, "radio4"))

        self.pushButton.clicked.connect(self.printPressed)

    def printPressed(self):

        if self.buttonGroup.checkedId() == -2:
            kolKartica = 2
        elif self.buttonGroup.checkedId() == -3:
            kolKartica = 4
        else:
            print("No radio button is selected")

        printaj(kolKartica)

        self.parent().setCurrentIndex(3)
