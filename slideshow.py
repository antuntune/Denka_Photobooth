from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QComboBox, QFileDialog, QLineEdit, QMessageBox
from PyQt5 import uic
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import random, os
import json

class SlideshowUi(QMainWindow):
    def __init__(self):

        super(SlideshowUi, self).__init__()
        uic.loadUi("slideshow.ui", self)

        self.initJsonVar()


        self.image_paths = []  # Initialize an empty list of image paths
        self.current_image_index = 0

        self.check_and_start_timer = QTimer(self)
        self.check_and_start_timer.timeout.connect(self.check_and_start_slideshow)
        self.check_and_start_timer.start(3000)  # Check every 3 seconds

        self.slideshow_timer = QTimer(self)
        self.slideshow_timer.timeout.connect(self.change_image)

    def get_image_paths(self):
        #current_directory = os.path.dirname(os.path.abspath(__file__) )  # Get the current directory path
        current_directory = self.EventAlbumPath + "picAlbum"
        image_files = [f for f in os.listdir(current_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        return [os.path.join(current_directory, image) for image in image_files]

    def check_and_start_slideshow(self):
        updated_image_paths = self.get_image_paths()  # Get the updated list of image paths

        if len(updated_image_paths) > 3:
            self.check_and_start_timer.stop()  # Stop the timer
            self.image_paths = updated_image_paths
            self.slideshow_timer.start(3000)  # Start the image change timer

    def change_image(self):
        if len(self.image_paths) <= 3:
            return  # Don't change images if there are 3 or fewer images

        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        image_path = self.image_paths[self.current_image_index]

        # Load the image and scale it to fit the label while preserving the aspect ratio
        pixmap = self.load_and_scale_image(image_path, self.slideshowLabel.size())

        #pixmap = QPixmap(image_path)

        self.slideshowLabel.setPixmap(pixmap)
        self.slideshowLabel.setAlignment(Qt.AlignCenter)


    def load_and_scale_image(self, image_path, label_size):
        image = QImage(image_path)
        if image.isNull():
            return QPixmap()  # Return an empty QPixmap if the image couldn't be loaded

        # Scale the image while preserving its aspect ratio to fit the label
        scaled_image = image.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Convert the scaled QImage to a QPixmap for displaying in the label
        pixmap = QPixmap.fromImage(scaled_image)

        return pixmap


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