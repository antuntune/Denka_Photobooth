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
import dslr
import io
from PyQt5.QtCore import Qt
import config_data




class ConfigUi(QMainWindow):
    def __init__(self):
        super(ConfigUi, self).__init__()
        uic.loadUi("res/ui/config.ui", self)

        self.shutdownButton.clicked.connect(self.shutdownApp)
        self.startButton.clicked.connect(self.startPressed)

        self.eventIDsList = self.findChild(QComboBox, 'eventIDsList')
        self.eventIDsList.currentIndexChanged.connect(self.eventIDsListIndexChanged)
        self.deleteID.clicked.connect(self.deleteIDFromList)
        self.addID.clicked.connect(self.addID2List)
        
        self.templateButton.clicked.connect(self.templatePath)
        self.albumButton.clicked.connect(self.lokacijaAlbuma)
        self.plusPrintButton.clicked.connect(self.increasePrintNum)
        self.minusPrintButton.clicked.connect(self.decreasePrintNum)
        self.cameraCheck.clicked.connect(self.cameraCheck_pressed)

        self.templateCheckBox.setEnabled(False)
        self.albumCheckBox.setEnabled(False)

        self.brightSlider.valueChanged.connect(self.changeBright)
        self.testAlbumCheckBox.stateChanged.connect(self.testAlbum_changed)

    def shutdownApp(self):
        QApplication.quit()

    def cameraCheck_pressed(self):
        cameraModel = dslr.get_camera_info()
        print(cameraModel)
        cameraShuuterCount = "\nCurrent Shutter Count: " + str(dslr.shutterCounter())
        text = str(cameraModel) + cameraShuuterCount
        self.cameraLabel.setText(text)

    def increasePrintNum(self):
        current = config_data.get_setting("printNum", 0)
        new_value = current + 2
        config_data.set_setting("printNum", new_value)
        self.printNumLabel.setText(str(new_value))

    def decreasePrintNum(self):
        current = config_data.get_setting("printNum", 0)
        new_value = max(2, current - 2)  # ne manje od 2
        config_data.set_setting("printNum", new_value)
        self.printNumLabel.setText(str(new_value))

    def testAlbum_changed(self, state):
        sender = self.sender()
        if sender.isChecked():
            config_data.set_setting("testAlbum", True)
            print("album true")
        else:
            config_data.set_setting("testAlbum", False)
            print("album false")

    def changeBright(self, value):
        config_data.set_setting("brightCorrection", str(value))
        self.brightLabel.setText(str(value))

    def addID2List(self):
        if len(self.inputID.text().strip()) < 3:
            QMessageBox.warning(self, "Greška", "Unos mora imati barem 3 znaka.")
            return
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Upozorenje!")
        msg_box.setText(f"Jeste li sigurni da želite dodati eventID: {self.inputID.text().strip()}")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg_box.exec_() == QMessageBox.Ok:
            config_data.add_event(self.inputID.text().strip())
            self.inputID.clear()
            self.initGUI()

    def deleteIDFromList(self):
        if self.eventIDsList.currentText() == "(Prazno)":
            QMessageBox.warning(self, "Greška", "Event ID lista je prazna.")
            return
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Upozorenje!")
        msg_box.setText(f"Jeste li sigurni da želite obrisati eventID: {self.inputID.text().strip()}")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg_box.exec_() == QMessageBox.Ok:
            config_data.delete_event(self.eventIDsList.currentText())
            #self.initGUI()
            self.refresh_eventIDsList()

    def refresh_eventIDsList(self):
        self.eventIDsList.clear()
        if config_data.get_event_ids():
            self.eventIDsList.addItems(config_data.get_event_ids())
        else:
            self.eventIDsList.addItem("(Prazno)")

    def eventIDsListIndexChanged(self, index):
        if not self.eventIDsList.currentText():
            return

        # Spremi trenutni event ID u bazu
        config_data.set_current_event_id(self.eventIDsList.currentText())

        # Dohvati podatke za trenutni event ID
        current_event_id = config_data.get_current_event_id()
        print(f"Trenutni event ID iz baze: {current_event_id}")

        # Dohvati podatke vezane za trenutni event
        event_data = config_data.get_event_data(current_event_id)
        print(f"Podaci za trenutni event: {event_data}")

        # Osvježi listu event ID-eva
        #self.refresh_eventIDsList()


    def initGUI(self):
        # Dohvati trenutni event ID
        current_event_id = config_data.get_current_event_id()
        
        if current_event_id:
            self.eventIDsList.setCurrentText(current_event_id)
        
        self.brightLabel.setText(str(config_data.get_setting("brightCorrection")))
        self.printNumLabel.setText(str(config_data.get_setting("printNum")))
        if config_data.get_setting("testAlbum"):
            self.testAlbumCheckBox.setCheckState(Qt.Checked)
        self.refresh_eventIDsList()

    def showEvent(self, event):
        self.initGUI()
        return super().showEvent(event)

    def lokacijaAlbuma(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            config_data.set_setting("album_path", folder_path)
            self.albumCheckBox.setCheckState(Qt.Checked)
            self.albumCheckBox.setText("Lokacija učitana")

    def templatePath(self):
        file_dialog = QFileDialog()
        template_path, _ = file_dialog.getOpenFileName(self, 'Odaberi sliku', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if not template_path:
            print("⚠️ Nije odabrana nijedna slika.")
            self.templateCheckBox.setCheckState(Qt.Unchecked)
            self.templateCheckBox.setText("Template nije učitan")
            return
        config_data.set_setting("templatePath", template_path)
        success = config_data.save_image_to_db(config_data.get_current_event_id(), template_path, "print_image")
        if not success:
            print("❌ Neuspjelo spremanje slike.")
            return

    def runSh(self):
        script_path = os.getcwd() + "/modprobe.sh"
        subprocess.run(['sh', script_path], check=True)

    def checkConditions4Start(self):
        if self.eventIDsList.currentText() == "(Prazno)":
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Upozorenje!")
            msg_box.setText("Event ID lista je prazna.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return False
        return True

    def startPressed(self):
        if not self.checkConditions4Start():
            return
        self.createEventMap()
        self.parent().setCurrentIndex(1)

    def createEventMap(self):
        directory = config_data.get_setting("album_path") + "/" + config_data.get_current_event_id()
        config_data.set_setting("working_dir_path", directory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        directory = config_data.get_setting("working_dir_path") + "/Album"
        if not os.path.exists(directory):
            os.makedirs(directory)

        directory = config_data.get_setting("working_dir_path") + "/testAlbum"
        if not os.path.exists(directory):
            os.makedirs(directory)