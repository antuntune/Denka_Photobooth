from PyQt5.QtWidgets import QMainWindow, QComboBox, QFileDialog, QLineEdit, QMessageBox, QCheckBox, QApplication
from PyQt5.QtGui import QColor  # This line is necessary to import QColor
from PyQt5 import uic
import qrcode
import json
import subprocess
import os
import shutil
from PIL import Image
import cups
import time
from slideshow import SlideshowUi


# spajanje na cups
conn = cups.Connection()
printers = conn.getPrinters()
# printers is a dictionary containing information about all the printers available

emptyDict = {}
AvailablePrinters = list(printers.keys())
PrinterUsing = AvailablePrinters[0]



class ConfigUi(QMainWindow):
    def __init__(self, arduinoInstance):
        
        self.slideshowUi = SlideshowUi()

        super(ConfigUi, self).__init__()
        uic.loadUi("res/ui/config.ui", self)

        self.initJsonVar()

        self.combobox = self.findChild(QComboBox, 'comboBox')
        self.combobox.addItems(self.eventId_)
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.onComboBoxIndexChanged)
        self.pushButton.clicked.connect(self.buttonPressed)

        # Slideshow button
        self.slideshowButton.clicked.connect(self.slideshow)

        self.arduinoTest.clicked.connect(self.arduinoTestButton)
        self.arduino = arduinoInstance
        self.status = False  # Initialize the status attribute

        self.karticaButton.clicked.connect(self.odaberiKarticu)
        self.albumButton.clicked.connect(self.lokacijaAlbuma)
        self.deleteID.clicked.connect(self.deleteWarning)
        self.addID.clicked.connect(self.addWarning)

        self.albumLabel.setWordWrap(True)
        self.promotivnaButton.clicked.connect(self.printajPromotivne)

        self.brightSlider.valueChanged.connect(self.changeBright)
        self.brightSlider.setValue(int(self.cardBright))
        self.brightLabel.setText(self.cardBright)

        # Connect checkboxes to a slot
        self.ArduinoCheckBox.stateChanged.connect(self.arduinocheckbox_changed)
        if self.arduinoStatus == True:
            self.ArduinoCheckBox.setChecked(True)


        self.WhatsAppCheckBox.stateChanged.connect(self.whatsappcheckbox_changed)
        if self.whatsapp == "1":
            self.WhatsAppCheckBox.setChecked(True)


    def slideshow(self):
        self.slideshowUi.show()


    def arduinoTestButton(self):
        self.testArduinoConnection()        

    def testArduinoConnection(self):
        if self.arduinoStatus:
            self.arduinoTest.hide()
            QApplication.processEvents()
            self.status = self.arduino.establishConnection()

            if self.status:
                # Create a QColor object using RGB values
                greenColor = QColor(0, 255, 0)
                self.arduinoLabel.setStyleSheet(f"background-color: {greenColor.name()}; color: white;")
                self.arduinoLabel.setText("Arduino je uspješno povezan.")
            else:
                # Create a QColor object using RGB values
                greenColor = QColor(255, 0, 0)
                self.arduinoLabel.setStyleSheet(f"background-color: {greenColor.name()}; color: white;")
                self.arduinoLabel.setText("Arduino se nije uspio povezati..")
        else:
            # Create a QColor object using RGB values
            greenColor = QColor(150, 100, 25)
            self.arduinoLabel.setStyleSheet(f"background-color: {greenColor.name()}; color: white;")
            self.arduinoLabel.setText("Stavi kvačicu na check box Arduino:")
        self.arduinoTest.show()
        QApplication.processEvents()

    def arduinocheckbox_changed(self, state):
        sender = self.sender()

        if sender.isChecked():
            self.arduinoStatus = True
            self.arduinocheckbox = True
        else:
            self.arduinoStatus = False
            self.arduinocheckbox = False
            # Create a QColor object using RGB values
            greenColor = QColor(0, 0, 0)
            self.arduinoLabel.setStyleSheet(f"background-color: {greenColor.name()};")


    def whatsappcheckbox_changed(self, state):
        sender = self.sender()

        if sender.isChecked():
            self.whatsapp = "1"
        else:
            self.whatsapp = "0"




    def changeBright(self, value):
        self.cardBright = str(value)
        self.brightLabel.setText(self.cardBright)

    def deleteWarning(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Upozorenje!")
        msg_box.setText("Jeste li sigurni da želite obrisati eventID: " + self.eventId)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        button_clicked = msg_box.exec_()
        if button_clicked == QMessageBox.Ok:
            self.eventId_.remove(self.eventId)
            self.combobox.clear()
            self.combobox.addItems(self.eventId_)
            print("Change confirmed.")
        else:
            print("Change canceled.")

    def addWarning(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Upozorenje!")
        msg_box.setText("Jeste li sigurni da želite dodati eventID: " + self.inputID.text())
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        button_clicked = msg_box.exec_()
        if button_clicked == QMessageBox.Ok:
            newEventID = self.inputID.text()
            self.inputID.clear()
            self.eventId_.append(newEventID)
            self.combobox.clear()
            self.combobox.addItems(self.eventId_)
            print("Change confirmed.")
        else:
            print("Change canceled.")


    # kad se prikaze ekran
    def showEvent(self, event):

        self.arduinocheckbox = self.arduinoStatus
        if self.arduinoStatus:
            self.testArduinoConnection()

        self.albumLabel.setText(self.albumPath)
        card_name = os.path.basename(self.cardPath)
        self.cardLabel.setText(card_name)
        self.cardLabel.setText(card_name)

        return super().showEvent(event)

    def lokacijaAlbuma(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(self, 'Select Folder')
        self.albumPath = folder_path
        self.albumPath = self.albumPath + "/" + "Albumi dogadaja/"
        self.albumLabel.setText(self.albumPath)
        

    def odaberiKarticu(self):
        file_dialog = QFileDialog()
        kartica_path, _ = file_dialog.getOpenFileName(self, 'Select File')
        self.cardPath = kartica_path
        if self.cardPath:
            card_name = os.path.basename(self.cardPath)
            self.cardLabel.setText(card_name)

    def printajPromotivne(self):

        im1 = Image.open("promotivna.jpg")

        def get_concat_h(im1):
            dst = Image.new('RGB', (im1.width + im1.width + 35, im1.height))
            dst.paste(im1, (35, 0))
            dst.paste(im1, (im1.width + 35, 0))
            return dst

        get_concat_h(im1).save("promotivnaFinished.jpg")

        conn.printFile(
            PrinterUsing, "promotivnaFinished.jpg", "title", emptyDict)
        conn.printFile(
            PrinterUsing, "promotivnaFinished.jpg", "title", emptyDict)



    def initJsonVar(self):
        # ucitavanje config.jsona i metanje u varijable da se lakse koristi
        with open('config.json', 'r') as f:
            # Load the contents of the file into a dictionary
            config = json.load(f)
            self.eventId_ = config['eventId_']
            self.tema_ = config['tema_']

        self.eventId = self.eventId_[0]
        self.tema = self.tema_[0]
        self.EventAlbumPath = config['eventAlbumPath']
        self.albumPath = config['albumPath']
        self.cardPath = config['cardPath']
        self.cardBright = config['cardBright']
        self.arduinoStatus = config['Arduino']
        self.whatsapp = config['WhatsApp']


    def onComboBoxIndexChanged(self, index):
        # update selected event to variable
        self.eventId = self.combobox.currentText()
        index = self.eventId_.index(self.eventId)
        element = self.eventId_.pop(index)  # Remove the element from its original position
        self.eventId_.insert(0, element)  # Insert the element at the beginning of the array
        print(" index eventaid : ", index)

    def loadJson(self):
        self.eventAlbumPath = self.albumPath + self.eventId + "/"
        #self.cardPath = self.eventAlbumPath + "/" + self.eventId + ".jpg"
        # Create a dictionary with the specific key-value pair
        data = {
            "eventId_": self.eventId_,
            "tema_": self.tema_,
            "eventId": self.eventId,
            "tema": self.tema,
            "albumPath": self.albumPath,
            "eventAlbumPath": self.eventAlbumPath,
            "cardPath": self.cardPath,
            "cardBright": self.cardBright,
            "Arduino": self.arduinoStatus,
            "WhatsApp": self.whatsapp
        }

        # Write data to the JSON file
        with open("config.json", "w") as file:
            json.dump(data, file)

    def runSh(self):

        script_path = os.getcwd() + "/modprobe.sh"
        subprocess.run(['sh', script_path], check=True)


    def buttonPressed(self):
        if not self.status and self.arduinocheckbox:
            self.testArduinoConnection()
            if not self.status:
                self.acknowledge = self.arduinoPupup()
                if self.acknowledge:
                    self.loadJson()
                    self.createEventMap()
                    self.napraviQr()
                    self.copyEventCard()
                    self.runSh()
                    self.parent().setCurrentIndex(1)
            else:
                time.sleep(4)
                self.loadJson()
                self.createEventMap()
                self.napraviQr()
                self.copyEventCard()
                self.runSh()
                self.parent().setCurrentIndex(1)

        else :
            self.loadJson()
            self.createEventMap()
            self.napraviQr()
            self.copyEventCard()
            self.runSh()
            self.parent().setCurrentIndex(2)


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
        #shutil.copy2(os.getcwd() +"/res/cardPool/" + self.eventId + ".jpg", self.albumPath + self.eventId)
        shutil.copy2(self.cardPath, self.albumPath + self.eventId)


    def arduinoPupup(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Upozorenje!")
        msg_box.setText("Arduino se nije uspio spojiti. Jeste li sigurni da želite nastaviti.")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        button_clicked = msg_box.exec_()
        if button_clicked == QMessageBox.Ok:
            print("Change confirmed.")
            return True
        else:
            print("Change canceled.")
            return False
            