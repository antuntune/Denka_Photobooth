from PyQt5.QtWidgets import QMainWindow, QComboBox, QFileDialog, QLineEdit, QMessageBox, QCheckBox, QApplication
from PyQt5.QtGui import QColor  # This line is necessary to import QColor
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import qrcode
import json
import subprocess
import os
import shutil
from PIL import Image
import cups
import time
from slideshow import SlideshowUi
from share_server import startServer
import dslr
import time
from share_server import update_predefined_text

# spajanje na cups
conn = cups.Connection()
printers = conn.getPrinters()
# printers is a dictionary containing information about all the printers available

emptyDict = {}
AvailablePrinters = list(printers.keys())
PrinterUsing = AvailablePrinters[0]


class ServerThread(QThread):
    started = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.server_started = False

    def run(self):
        if not self.server_started:
            startServer()
            self.server_started = True
            self.started.emit()

class ConfigUi(QMainWindow):
    def __init__(self):
        
        self.slideshowUi = SlideshowUi()

        super(ConfigUi, self).__init__()
        uic.loadUi("res/ui/config.ui", self)

        self.initJsonVar()

        self.combobox = self.findChild(QComboBox, 'comboBox')
        self.combobox.addItems(self.eventId_)
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.onComboBoxIndexChanged)
        self.pushButton.clicked.connect(self.buttonPressed)
        self.saveButton.clicked.connect(self.savePressed)

        self.shareButton.clicked.connect(self.popout_terminal_and_execute)

        self.cameraCheck.clicked.connect(self.cameraCheck_pressed)

        # Slideshow button
        self.slideshowButton.clicked.connect(self.slideshow)

        self.karticaButton.clicked.connect(self.odaberiKarticu)
        self.albumButton.clicked.connect(self.lokacijaAlbuma)
        self.deleteID.clicked.connect(self.deleteWarning)
        self.addID.clicked.connect(self.addWarning)

        self.albumLabel.setWordWrap(True)
        self.promotivnaButton.clicked.connect(self.printajPromotivne)

        self.brightSlider.valueChanged.connect(self.changeBright)
        self.brightSlider.setValue(int(self.cardBright))
        self.brightLabel.setText(self.cardBright)

        self.picNumSlider.valueChanged.connect(self.picNum)
        self.picNumSlider.setValue(int(int(self.print_limit_num)/2))
        self.picNumLabel.setText(str(self.print_limit_num))

        self.cameraPortComboBox.addItem("0")
        self.cameraPortComboBox.addItem("1")
        self.cameraPortComboBox.addItem("2")

        # Connect the currentIndexChanged signal to the on_combobox_changed slot
        self.cameraPortComboBox.currentIndexChanged.connect(self.cameraPort_changed)

        # Connect checkboxes to a slot
        self.shareImagesCheckBox.stateChanged.connect(self.shareImages_changed)
        if self.shareImages == True:
            self.shareImagesCheckBox.setChecked(True)

        # Connect checkboxes to a slot
        self.testAlbumCheckBox.stateChanged.connect(self.testAlbum_changed)
        if self.testAlbum == True:
            self.testAlbumCheckBox.setChecked(True)

    def cameraPort_changed(self, index):
        self.cameraPort = self.cameraPortComboBoxs.currentText()
        print("Selected:", self.cameraPort)

    def cameraCheck_pressed(self):
        cameraModel = dslr.get_camera_info()
        print(cameraModel)
        cameraShuuterCount = "\nCurrent Shutter Count: " + str(dslr.shutterCounter())
        text = str(cameraModel)  + cameraShuuterCount
        self.cameraLabel.setText(text)

    def popout_terminal_and_execute(self):
        # Command to execute
        command = "ngrok http --domain denka.ngrok.app 5001"
        # Replace 'gnome-terminal' with the terminal emulator of your choice
        terminal_emulator = 'gnome-terminal'
        # Replace 'bash' with the shell you want to use in the new terminal window
        shell = 'bash'
        process = subprocess.Popen([terminal_emulator, '--', shell, '-c', command])

    def slideshow(self):
        self.slideshowUi.show()

    def picNum(self, value):
        self.pic_num_print_limit = str(value * 2)
        self.print_limit_num = int(value * 2)
        self.picNumLabel.setText(self.pic_num_print_limit)

    def testAlbum_changed(self, state):
        sender = self.sender()

        if sender.isChecked():
            self.testAlbum = True
        else:
            self.testAlbum = False

    def shareImages_changed(self, state):
        sender = self.sender()

        if sender.isChecked():
            self.shareImages = True
        else:
            self.shareImages = False


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
        self.albumLabel.setText(self.albumPath)
        card_name = os.path.basename(self.cardPath)
        self.cardLabel.setText(card_name)
        self.cardLabel.setText(card_name)
        self.server_thread = ServerThread()
        self.server_thread.start()
        self.comboBox.setCurrentIndex(int(self.cameraPort))
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
        self.testAlbum = config['testAlbum']
        self.print_limit_num = config['print_limit_num']
        self.shareImages = config['shareImages']
        self.cameraPort =config['cameraPort']


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
            "testAlbum": self.testAlbum,
            "print_limit_num": self.print_limit_num,
            "shareImages": self.shareImages,
            "cameraPort": self.cameraPort
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
            self.copyEventCard()
            self.runSh()
            self.parent().setCurrentIndex(1)

    def savePressed(self):
        self.loadJson()

    def createEventMap(self):
        directory = ""
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

        # unutar mape događaja kreiraj mapu za slike
        directory = self.albumPath + self.eventId + "/testAlbum"
        if not os.path.exists(directory):
            os.makedirs(directory)

    def copyEventCard(self):
        # kopiraj karticu dogadaja u mapu dogadaja
        #shutil.copy2(os.getcwd() +"/res/cardPool/" + self.eventId + ".jpg", self.albumPath + self.eventId)
        print("Album Path:", self.albumPath)
        print("Event ID:", self.eventId)

        shutil.copy2(self.cardPath, self.albumPath + self.eventId)