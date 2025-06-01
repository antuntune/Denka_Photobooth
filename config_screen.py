
from PyQt5.QtWidgets import QMainWindow, QComboBox, QFileDialog, QLineEdit, QMessageBox, QCheckBox, QApplication, QLabel, QDialog, QVBoxLayout
from PyQt5.QtGui import QColor, QPixmap, QImage  # This line is necessary to import QColor
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QImage

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
import logging
import config_data
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray
from io import BytesIO



class QLabelLogHandler(logging.Handler):
    def __init__(self, label: QLabel):
        super().__init__()
        self.label = label

    def emit(self, record):
        # Get the log message
        msg = self.format(record)
        
        # Add color based on log level
        if record.levelname == 'DEBUG':
            msg = f'<font color="white">{msg}</font>'
        elif record.levelname == 'INFO':
            msg = f'<font color="blue">{msg}</font>'
        elif record.levelname == 'WARNING':
            msg = f'<font color="yellow">{msg}</font>'
        elif record.levelname == 'ERROR':
            msg = f'<font color="red">{msg}</font>'
        elif record.levelname == 'CRITICAL':
            msg = f'<font color="darkred">{msg}</font>'

        # Get the current text of the QLabel
        current_text = self.label.text()

        # Add the new message at the top of the current text
        new_text = msg + '<br>' + current_text
        
        # Update the QLabel text (this will add new messages at the top)
        self.label.setText(new_text)
        self.label.repaint()  # Repaint to update the QLabel immediately




class ConfigUi(QMainWindow):
    cursorVisibilityChanged = pyqtSignal(bool)  # Define the signal
    def __init__(self):
        super(ConfigUi, self).__init__()
        uic.loadUi("res/ui/config.ui", self)

        self.cursorCheckBox.stateChanged.connect(self.emit_cursor_change)
        self.cursorCheckBox.setChecked(True)  # Initial state of the checkbox

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

        # Create a custom log handler
        log_handler = QLabelLogHandler(self.log_label)
        log_handler.setLevel(logging.DEBUG)
        
        # Create a logger and add the custom handler
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)

    # Function to handle image display:
    def show_image(self, template_image_blob):
        try:
            if template_image_blob:
                # Convert the BLOB data to QPixmap
                pixmap = self.convert_blob_to_pixmap(template_image_blob)
                
                # Save the pixmap as a temporary file or handle it directly in a dialog
                image_path = "/path/to/save/temp_image.png"
                pixmap.save(image_path)

                # Show the image in a separate dialog
                image_dialog = ImageDialog(image_path)
                image_dialog.exec_()  # Show the dialog
            else:
                print("No template image found.")
                # You could also show a message box here if needed
        except ValueError as e:
            print(f"Error loading image: {e}")

    def generate_log(self):
        # Generate some log messages
        logging.debug("This is a debug message")
        logging.info("This is an info message")
        logging.warning("This is a warning message")
        logging.error("This is an error message")
        logging.critical("This is a critical message")

    def emit_cursor_change(self):
        hide = not self.cursorCheckBox.isChecked()
        self.cursorVisibilityChanged.emit(hide)  # Emit the signal with the checkbox state

    def shutdownApp(self):
        QApplication.quit()

    def cameraCheck_pressed(self):
        cameraModel = dslr.get_camera_info()
        print(cameraModel)
        cameraShuuterCount = "\nCurrent Shutter Count: " + str(dslr.shutterCounter())
        text = str(cameraModel) + cameraShuuterCount
        self.cameraLabel.setText(text)

    def increasePrintNum(self):
        try:
            current = int(config_data.get_setting("max_print_per_seq", 0))  # Attempt to convert to integer
        except ValueError:
            current = 0  # Default to 0 if there's an error

        new_value = current + 2
        config_data.set_setting("max_print_per_seq", new_value)
        self.printNumLabel.setText(str(new_value))

        logging.info(f"Increased print number to {new_value}")

    def decreasePrintNum(self):
        current = int(config_data.get_setting("max_print_per_seq", 0))
        new_value = max(2, current - 2)  # Don't go below 2
        config_data.set_setting("max_print_per_seq", new_value)
        self.printNumLabel.setText(str(new_value))

        logging.info(f"Decreased print number to {new_value}")


    def testAlbum_changed(self, state):
        sender = self.sender()
        if sender.isChecked():
            config_data.set_setting("test_album", 1)  # True za označeno
            #print("album true")
        else:
            config_data.set_setting("test_album", 0)  # False za neoznačeno
            #print("album false")
        

    def changeBright(self, value):
        config_data.set_setting("brightness", str(value))
        self.brightLabel.setText(str(value))

    def ____addID2List(self):
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
            self.refresh_eventIDsList()

    def ___deleteIDFromList(self):
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
            self.refresh_eventIDsList()

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
            logging.info(f"Deleted event ID: {self.eventIDsList.currentText()}")
            self.refresh_eventIDsList()


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
            logging.info(f"Added event ID: {self.inputID.text().strip()}")
            self.inputID.clear()
            self.refresh_eventIDsList()

            


    def refresh_eventIDsList(self):
        print(config_data.get_current_event_id())
        self.eventIDsList.clear()
        event_ids = config_data.get_event_ids()
        if event_ids:
            self.eventIDsList.addItems(event_ids)
            event_ids.insert(0, config_data.get_current_event_id())
        else:
            self.eventIDsList.addItem("(Prazno)")


    def eventIDsListIndexChanged(self, index):
        # Provjeri da li je trenutni odabrani event ID različit od prethodnog
        self.current_event_id = self.eventIDsList.currentText()
        config_data.set_current_event_id(self.current_event_id)
        # Ako je odabrani event ID isti kao prethodni, ne radi ništa
        if self.current_event_id == "(Prazno)":
            return
        if self.current_event_id != "":
            # Dohvati podatke vezane za trenutni event
            #event_data = config_data.get_event_data()
            self.initGUI()


    def initGUI(self):
        
        current_event_id = config_data.get_current_event_id()  # Dohvati trenutni event_id
        # Ako je odabrani event ID isti kao prethodni, ne radi ništa
        if current_event_id == "(Prazno)":
            return
        if current_event_id != "":
            event_data = config_data.get_event_data()
            # Dohvaćanje specifične postavke 'test_album' za trenutni event_id
            test_album = config_data.get_setting("test_album", False)  # Ako nije pronađeno, vraća False
            # Dohvati brightness za trenutni event_id koristeći get_setting
            brightness = config_data.get_setting("brightness", None)  # Ako nije pronađeno, vraća None
            self.brightLabel.setText(str(brightness))
            self.brightSlider.setValue(int(brightness))
            self.printNumLabel.setText(str(config_data.get_setting("max_print_per_seq")))
            if bool(config_data.get_setting("test_album", False)):
                self.testAlbumCheckBox.setCheckState(Qt.Checked)
            else:
                self.testAlbumCheckBox.setCheckState(Qt.Unchecked)

            template_image=config_data.get_setting("template_image", None)
            #print(template_image)
            #print(f"template image : {template_image}")
            if template_image!=None:  # If template_image has a value (not None or empty)
                    self.templateCheckBox.setCheckState(Qt.Checked)
            if template_image == None:
                self.templateCheckBox.setCheckState(Qt.Unchecked)

            album_location = config_data.get_setting('album_location', None)  # Safely get template_image
            if album_location:  # If template_image has a value (not None or empty)
                self.albumCheckBox.setCheckState(Qt.Checked)
            if album_location== None:
                self.albumCheckBox.setCheckState(Qt.Unchecked)


    def showEvent(self, event):
        self.generate_log()
        self.refresh_eventIDsList()
        self.initGUI()
        return super().showEvent(event)

    def lokacijaAlbuma(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            config_data.set_setting("album_location", folder_path)
            self.albumCheckBox.setCheckState(Qt.Checked)


    def templatePath(self):
        try:
            file_dialog = QFileDialog()
            template_path, _ = file_dialog.getOpenFileName(self, 'Odaberi sliku', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
            if not template_path:
                self.templateCheckBox.setCheckState(Qt.Unchecked)
                return
            
            success = config_data.save_image_to_db(template_path, "template_image")
            if not success:
                logging.error(f"Failed to save the image: {template_path}")
                return

            logging.info(f"Template image loaded successfully: {template_path}")
            self.templateCheckBox.setCheckState(Qt.Checked)
        except Exception as e:
            logging.error(f"Error loading template image: {str(e)}", exc_info=True)


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
        try:
            directory = config_data.get_setting("album_location") + "/" + config_data.get_current_event_id()

            #config_data.set_setting("working_dir_path", directory)
            print(directory)
            
            if not os.path.exists(directory):
                os.makedirs(directory)

            if not os.path.exists(directory + "/Album"):
                os.makedirs(directory + "/Album")

            if not os.path.exists(directory + "/testAlbum"):
                os.makedirs(directory + "/testAlbum")

            logging.info(f"Created directories for event: {config_data.get_current_event_id()}")
        except Exception as e:
            logging.error(f"Error creating event directories: {str(e)}", exc_info=True)
