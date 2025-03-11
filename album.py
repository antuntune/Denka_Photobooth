from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QShowEvent
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
import json
import cloudinary
import time
import os
from cloudinary.uploader import upload
from PIL import Image
import qrcode
import secrets
import string

# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Thread class for handling a timeout period, used for the splash screen


class TimeOutThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        time.sleep(60)  # Timeout for splash screen
        self.finished.emit()  # Emit the 'finished' signal when the work is done

# Thread class for handling image uploads to Cloudinary


class UploadThread(QThread):
    finished = pyqtSignal()  # Custom signal to indicate thread completion

    def __init__(self, images, event_id, random_string, parent=None):
        super().__init__(parent)
        self.images = images
        self.event_id = event_id
        self.random_string = random_string

    def run(self):
        # Upload each image to Cloudinary
        for i, image in enumerate(self.images, start=1):
            upload(
                image, public_id=f"denka/{self.event_id}/{self.random_string}/slika{i}")
        # Upload the GIF to Cloudinary
        upload("images/output.gif",
               public_id=f"denka/{self.event_id}/{self.random_string}/zx")
        self.finished.emit()  # Emit the 'finished' signal when the work is done

# Main window class for the album UI


class AlbumUi(QMainWindow):
    def __init__(self):
        super(AlbumUi, self).__init__()

        self.loaded_resources = False  # Flag to check if resources are loaded
        self.eventId = ""  # Event ID placeholder
        self.timeout_thread = TimeOutThread(parent=self)
        # Connect timeout thread signal to slot
        self.timeout_thread.finished.connect(self.timeoutThreadFinished)

    def timeoutThreadFinished(self):
        # Set the current index to 1 on the parent widget when timeout finishes
        self.parent().setCurrentIndex(1)

    def loadFromJson(self):
        # Load configuration from JSON file
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.eventId = config['eventId']
            self.tema = config['tema']
            self.albumPath = config['albumPath']
            self.eventAlbumPath = config['eventAlbumPath']
            self.cardPath = config['cardPath']

    def loadResources(self):
        # Load UI resources based on the theme specified in the config
        uic.loadUi(os.getcwd() + "/res/ui/" + self.tema + "/album.ui", self)
        # Connect the push button to the sharePressed method
        self.pushButton.clicked.connect(self.sharePressed)

    def showEvent(self, a0: QShowEvent) -> None:
        if not self.loaded_resources:
            self.loadFromJson()  # Load configuration
            self.loadResources()  # Load UI resources
            self.loaded_resources = True  # Mark resources as loaded

        # Generate a random string for unique identification
        def generate_random_string(length):
            characters = string.ascii_letters + string.digits
            return ''.join(secrets.choice(characters) for _ in range(length))

        random_string = generate_random_string(10)
        print(random_string)

        # Create a GIF from a list of image files
        image_filenames = ['images/slika1.jpg',
                           'images/slika2.jpg', 'images/slika3.jpg']
        duration = 500  # Duration for each frame in milliseconds (0.5 seconds)
        images = [Image.open(filename) for filename in image_filenames]
        # Convert images to RGBA mode
        images = [image.convert('RGBA') for image in images]
        images[0].save('images/output.gif', save_all=True,
                       append_images=images[1:], duration=duration, loop=0)

        # Generate a QR code for a dynamic URL
        url = f"https://www.denka.com.hr/img?folder={self.eventId}/{random_string}"
        qr_image = qrcode.make(url)
        qr_image.save("qr.png")
        print(url)

        # Display the QR code in the QLabel widget
        self.qr = self.findChild(QLabel, 'qr')
        qrPixmap = QPixmap("qr.png")
        self.qr.setPixmap(qrPixmap)

        # Start the timeout thread
        self.timeout_thread.start()

        # Start the upload thread
        self.upload_thread = UploadThread(
            image_filenames, self.eventId, random_string, parent=self)
        # Connect upload thread signal to slot
        self.upload_thread.finished.connect(self.uploadThreadFinished)
        self.upload_thread.start()

        return super().showEvent(a0)

    def uploadThreadFinished(self):
        # Method called when the upload thread finishes
        print("Upload completed.")

    def sharePressed(self):
        # Terminate the timeout thread if the share button is pressed
        self.timeout_thread.terminate()
        # Change to the next screen in the parent widget
        self.parent().setCurrentIndex(1)

    def uploadToAlbum(self, brojSlike, eventId):
        # Upload image to album
        upload(self.eventAlbumPath + "slika" + str(brojSlike) + ".jpg",
               public_id="djenka/" + self.eventId + "/album/" + str(time.time()))
