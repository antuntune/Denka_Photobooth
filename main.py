#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import os
import sys
import json
from config_screen import ConfigUi
from splash import SplashUi
from camera import CameraUi
from print import PrintUi

from album import AlbumUi
import res


app = QApplication(sys.argv)

widget = QStackedWidget()

splashUi = SplashUi()
cameraUi = CameraUi()
printUi = PrintUi()
albumUi = AlbumUi()
configUi = ConfigUi()

widget.addWidget(configUi)

widget.addWidget(splashUi)

widget.addWidget(cameraUi)

widget.addWidget(printUi)

#widget.addWidget(shareUi)

widget.addWidget(albumUi)

# Connect the cursorVisibilityChanged signal from configUi to a slot
def update_cursor_visibility(hide):
    if hide:
        app.setOverrideCursor(QCursor(Qt.BlankCursor))  # Hide the cursor
    else:
        app.restoreOverrideCursor()  # Restore the cursor visibility

# Connecting signal to the slot
configUi.cursorVisibilityChanged.connect(update_cursor_visibility)

widget.showFullScreen()
app.exec_()