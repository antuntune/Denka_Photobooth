#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
import sys
import res
import json
import subprocess
import importlib
from splash import SplashUi
from camera import CameraUi
from print import PrintUi
from album import AlbumUi
from config import ConfigUi
import os

# pravi mapu session ako je jos nema
directory = 'res/session'
if not os.path.exists(directory):
    os.makedirs(directory)

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']
tema = config['tema']

# konvertiranje qrc u py, zakomentirano jer  ga jebe memorija

# qrc_file = 'res/ui/'+tema+'/res.qrc'
# pyres_file = 'res.py'
# subprocess.run(['pyrcc5', qrc_file, '-o', pyres_file])
# importlib.reload(res)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

configUi = ConfigUi()

# radi i bez tog ??
# configUi.setParent(widget)
widget.addWidget(configUi)

splashUi = SplashUi()
widget.addWidget(splashUi)

cameraUi = CameraUi()
widget.addWidget(cameraUi)

printUi = PrintUi()
widget.addWidget(printUi)

albumUi = AlbumUi()
widget.addWidget(albumUi)

widget.showFullScreen()
app.exec_()
