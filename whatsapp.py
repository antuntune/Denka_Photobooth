from PyQt5.QtWidgets import QMainWindow, QLabel, QButtonGroup, QRadioButton, QDialog
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QUrl
from PyQt5.QtMultimedia import QSoundEffect
import json
import cloudinary
import time, os
from cloudinary.uploader import upload
import importlib
import threading
#import pywhatkit



class CustomWidgetPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.number = ""

        # Load the UI file using loadUi
        uic.loadUi(os.getcwd() + "/res/ui/"+"denka"+"/keyboard.ui", self)  # Replace "widget.ui" with your UI file name

        self.pushButton_enter.clicked.connect(self.enter)
        self.pushButton.clicked.connect(self.num_1)
        self.pushButton_2.clicked.connect(self.num_2)
        self.pushButton_3.clicked.connect(self.num_3)
        self.pushButton_4.clicked.connect(self.num_4)
        self.pushButton_5.clicked.connect(self.num_5)
        self.pushButton_6.clicked.connect(self.num_6)
        self.pushButton_7.clicked.connect(self.num_7)
        self.pushButton_8.clicked.connect(self.num_8)
        self.pushButton_9.clicked.connect(self.num_9)

        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_backspace.clicked.connect(self.backspace)

        self.call_numbers = ["+385", "+43", "+49"]

        self.comboBox_prefix.addItems(self.call_numbers)
        self.comboBox_prefix.setCurrentIndex(0)
        self.comboBox_prefix.currentIndexChanged.connect(self.onComboBoxIndexChanged)


    def onComboBoxIndexChanged(self, index):
        # update selected event to variable
        self.call_number = self.comboBox_prefix.currentText()
        index = self.call_numbers.index(self.call_number)
        element = self.call_numbers.pop(index)  # Remove the element from its original position
        self.call_numbers.insert(0, element)  # Insert the element at the beginning of the array
        print(" call_number : ", index)

    def get_number(self):
        self.number = self.call_number + self.number
        return self.number  # Return the 'number' attribute value

    def enter (self):
        self.close()

    def num_1 (self):
        self.number = self.number + "1"
        self.label_number.setText(self.number)

    def num_2 (self):
        self.number = self.number + "2"
        self.label_number.setText(self.number)

    def num_3 (self):
        self.number = self.number + "3"
        self.label_number.setText(self.number)

    def num_4 (self):
        self.number = self.number + "4"
        self.label_number.setText(self.number)

    def num_5 (self):
        self.number = self.number + "5"
        self.label_number.setText(self.number)

    def num_6 (self):
        self.number = self.number + "6"
        self.label_number.setText(self.number)

    def num_7 (self):
        self.number = self.number + "7"
        self.label_number.setText(self.number)

    def num_8 (self):
        self.number = self.number + "8"
        self.label_number.setText(self.number)

    def num_9 (self):
        self.number = self.number + "9"
        self.label_number.setText(self.number)

    def clear (self):
        self.number = ""
        self.label_number.setText(self.number)

    def backspace (self):
        self.number = self.number[:-1]
        self.label_number.setText(self.number)

class TimeOutThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        time.sleep(90)  # Timeout for splash screen
        self.finished.emit()  # Emit the 'finished' signal when the work is done


class WhatsAppUi(QMainWindow):
    def __init__(self):
        super(WhatsAppUi, self).__init__()

        self.loaded_resources = False
        self.skipButtonPressed = False

        self.brojSlike = 1
        self.eventId = ""

        self.timeout_thread = TimeOutThread(parent=self)
        self.timeout_thread.finished.connect(self.timeoutThreadFinished)

        self.number = ""


    def show_custom_widget_popup(self):
        custom_widget_popup = CustomWidgetPopup()
        custom_widget_popup.setWindowModality(Qt.ApplicationModal)
        custom_widget_popup.exec_()

        # After the popup is closed, retrieve the 'number' from the child
        self.number = custom_widget_popup.get_number()

        self.label_number.setText(self.number)

    def timeoutThreadFinished(self):
        if self.skipButtonPressed == False:
            self.parent().setCurrentIndex(1)

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

    def loadResources(self):

        uic.loadUi(os.getcwd() + "/res/ui/"+self.tema+"/whatsapp.ui", self)

        # slike
        self.img1 = self.findChild(QLabel, 'img1')
        self.img2 = self.findChild(QLabel, 'img2')
        self.img3 = self.findChild(QLabel, 'img3')

        # radio
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio1"))
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio2"))
        self.buttonGroup.addButton(self.findChild(
            QRadioButton, "radio3"))

        # Button sound effect
        self.btn_sfx = QSoundEffect()
        self.btn_sfx.setSource(QUrl.fromLocalFile(os.getcwd() + '/res/ui/btn.wav'))
        self.pushButton.pressed.connect(self.btn_sfx.play)

        # button
        self.pushButton.clicked.connect(self.sharePressed)
        self.skipButton.clicked.connect(self.skipPressed)

        self.pushButton_keyboard.clicked.connect(self.show_custom_widget_popup)

    def showEvent(self, a0: QShowEvent) -> None:

        if not self.loaded_resources:
            self.loadFromJson()
            self.loadResources()
            self.loaded_resources = True

        self.skipButtonPressed = False

        img1pixmap = QPixmap(self.eventAlbumPath + "slika1.jpg")
        img2pixmap = QPixmap(self.eventAlbumPath + "slika2.jpg")
        img3pixmap = QPixmap(self.eventAlbumPath + "slika3.jpg")
        self.img1.setPixmap(img1pixmap)
        self.img2.setPixmap(img2pixmap)
        self.img3.setPixmap(img3pixmap)

        self.timeout_thread.start()

        return super().showEvent(a0)

    def sharePressed(self):
        # provjerava koji je radiobutton ukljucen
        if self.buttonGroup.checkedId() == -2:
            self.brojSlike = 1
        elif self.buttonGroup.checkedId() == -3:
            self.brojSlike = 2
        elif self.buttonGroup.checkedId() == -4:
            self.brojSlike = 3

        #self.uploadThread = threading.Thread(target = self.uploadToAlbum, args=(self.brojSlike, self.eventId))
        #self.uploadThread.start()

        #self.uploadToAlbum(self.brojSlike, self.eventId)

        # Send an Image to a Group with the Caption as Hello
        pywhatkit.sendwhats_image("+385977504846", "promotivna.png")

        self.skipButtonPressed = True

        self.parent().setCurrentIndex(5)

    def skipPressed(self):
        self.skipButtonPressed = True
        self.parent().setCurrentIndex(5)

    def uploadToAlbum(self, brojSlike, eventId):
        upload(self.eventAlbumPath + "slika" + str(brojSlike) + ".jpg",
               public_id="djenka/" + self.eventId + "/album/" + str(time.time()))


