#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import os
import sys
import json
from config import ConfigUi
from splash import SplashUi
from camera import CameraUi
from print import PrintUi
from album import AlbumUi
from whatsapp import WhatsAppUi
import res
from arduino_eye import ArduinoController



app = QApplication(sys.argv)

# hide cursor in app
#app.setOverrideCursor(QCursor(Qt.BlankCursor))	

widget = QStackedWidget()

arduino = ArduinoController()


splashUi = SplashUi()
cameraUi = CameraUi(arduino)
albumUi = AlbumUi()
whatsappUi = WhatsAppUi()
printUi = PrintUi()
configUi = ConfigUi(arduino)

widget.addWidget(configUi)

widget.addWidget(splashUi)


widget.addWidget(cameraUi)


widget.addWidget(albumUi)


widget.addWidget(whatsappUi)


widget.addWidget(printUi)


widget.showFullScreen()
app.exec_()