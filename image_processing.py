from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtMultimedia import QSoundEffect
from PIL import Image, ImageOps, ImageEnhance






def napraviKarticu(self):

    kartica = Image.open(self.cardPath)
    im1 = Image.open(self.eventAlbumPath + "/slika1.jpg").resize((892, 596))
    im2 = Image.open(self.eventAlbumPath + "/slika2.jpg").resize((892, 596))
    im3 = Image.open(self.eventAlbumPath + "/slika3.jpg").resize((892, 596))

    kartica.paste(im1, (54, 217))
    kartica.paste(im2, (54, 879))
    kartica.paste(im3, (54, 1541))

    # Promijeni svijetlinu kartice
    enhancer = ImageEnhance.Brightness(kartica)
    kartica = enhancer.enhance(int(self.cardBright)/100)

    # Šarpiraj ga malo
    enhancer = ImageEnhance.Sharpness(kartica)
    kartica = enhancer.enhance(5.0)


    kartica.save(self.eventAlbumPath + self.eventId + "finished" + ".jpg", quality=96)



    def renameImage(name):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith("jpg"):
                os.rename(filename, (name + ".jpg"))