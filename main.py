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
import res


app = QApplication(sys.argv)
app.setOverrideCursor(QCursor(Qt.BlankCursor))	

widget = QStackedWidget()

configUi = ConfigUi()

widget.addWidget(configUi)

splashUi = SplashUi()
widget.addWidget(splashUi)

cameraUi = CameraUi()
widget.addWidget(cameraUi)

albumUi = AlbumUi()
widget.addWidget(albumUi)

printUi = PrintUi()
widget.addWidget(printUi)













































































widget.showFullScreen()
app.exec_()
