

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QComboBox, QApplication
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from cloudinary.uploader import upload
import json
import time
import cloudinary
import cups
from PIL import Image

import cv2
import os
import keyboard
import queue
import pymongo
import qrcode
import sys
import res
import subprocess
import importlib

from splash import SplashUi
from camera import CameraUi
from print import PrintUi
from album import AlbumUi
from config import ConfigUi
import os


