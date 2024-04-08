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
from share import ShareUi
import res


app = QApplication(sys.argv)

# hide cursor in app
app.setOverrideCursor(QCursor(Qt.BlankCursor))	

widget = QStackedWidget()


splashUi = SplashUi()
cameraUi = CameraUi()
printUi = PrintUi()
shareUi = ShareUi()
configUi = ConfigUi()

widget.addWidget(configUi)

widget.addWidget(splashUi)

widget.addWidget(cameraUi)

widget.addWidget(printUi)

widget.addWidget(shareUi)

widget.showFullScreen()
app.exec_()