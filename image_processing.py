from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtMultimedia import QSoundEffect
from PIL import Image, ImageOps, ImageEnhance
import shutil, os
from datetime import datetime
from PIL import Image
from io import BytesIO



def renameImage(new_name, old_name):
    print(f"treba preimenovat {old_name} u novo immmmme {new_name}")
    os.rename(old_name, (new_name + ".jpg"))

def makeDoublePrintSeq(im, spacing=35):
    dst = Image.new('RGB', (im.width * 2 + spacing, im.height))
    dst.paste(im, (spacing, 0))
    dst.paste(im, (im.width + spacing, 0))
    return dst

def pil2pixmap(image):
    """Konvertiraj PIL.Image u QPixmap."""
    image = image.convert("RGBA")
    data = image.tobytes("raw", "RGBA")
    qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
    return QPixmap.fromImage(qimage)


def makePrintSeq():
    # Dohvati sve slike iz baze
    template_data = config_data.get_image_from_db("template_image")
    if template_data:
        try:
            image = Image.open(BytesIO(template_data))
            #image.show()  # Otvara zadani preglednik slika (e.g. Eye of GNOME, Xviewer)
        except Exception as e:
            print(f"Greška pri prikazu slike: {e}")
    else:
        print("❌ Nema slike u bazi.")

    img1_data = config_data.get_image_from_db("shot_img1")
    if template_data:
        try:
            image = Image.open(BytesIO(img1_data))
            #image.show()  # Otvara zadani preglednik slika (e.g. Eye of GNOME, Xviewer)
        except Exception as e:
            print(f"Greška pri prikazu slike: {e}")
    else:
        print("❌ Nema slike u bazi.")

    img2_data = config_data.get_image_from_db("shot_img2")
    if img2_data:
        try:
            image = Image.open(BytesIO(img2_data))
            #image.show()  # Otvara zadani preglednik slika (e.g. Eye of GNOME, Xviewer)
        except Exception as e:
            print(f"Greška pri prikazu slike: {e}")
    else:
        print("❌ Nema slike u bazi.")

    img3_data = config_data.get_image_from_db("shot_img3")
    if img3_data:
        try:
            image = Image.open(BytesIO(img3_data))
            #image.show()  # Otvara zadani preglednik slika (e.g. Eye of GNOME, Xviewer)
        except Exception as e:
            print(f"Greška pri prikazu slike: {e}")
    else:
        print("❌ Nema slike u bazi.")
    # Provjera
    if not all([template_data, img1_data, img2_data, img3_data]):
        print("❌ Nedostaje jedna ili više slika u bazi.")
        return

    # Učitaj slike iz binarnih podataka
    printSeqImg = Image.open(BytesIO(template_data))
    im1 = Image.open(BytesIO(img1_data)).resize((892, 596))
    im2 = Image.open(BytesIO(img2_data)).resize((892, 596))
    im3 = Image.open(BytesIO(img3_data)).resize((892, 596))
    # Zalijepi slike na template
    printSeqImg.paste(im1, (54, 217))
    printSeqImg.paste(im2, (54, 879))
    printSeqImg.paste(im3, (54, 1541))
    # Promijeni svjetlinu
    enhancer = ImageEnhance.Brightness(printSeqImg)
    printSeqImg = enhancer.enhance(int(config_data.get_setting("brightness")) / 100)
    # Oštri sliku
    enhancer = ImageEnhance.Sharpness(printSeqImg)
    printSeqImg = enhancer.enhance(5.0)
    shot_time = datetime.now().strftime("_%d-%m-%Y_%H:%M:%S")
    doublePrintSeqImg = makeDoublePrintSeq(printSeqImg)
    current_print_seq_path = config_data.get_setting("album_location") + "/" + config_data.get_current_event_id() + "/printSequences/printSeq_" + shot_time + ".jpg"
    config_data.set_setting("current_print_seq_path", current_print_seq_path)
    print(config_data.get_setting("current_print_seq_path"))
    print("iznad je current_print_seq_path")
    doublePrintSeqImg.save(current_print_seq_path, quality=96)
    printSeqImg = pil2pixmap(printSeqImg)
    return printSeqImg

def makeGif():
    # Dohvati slike iz baze (kao binarne podatke)
    img1_data = config_data.get_image_from_db("shot_img1")
    img2_data = config_data.get_image_from_db("shot_img2")
    img3_data = config_data.get_image_from_db("shot_img3")

    # Pretvori ih u PIL.Image objekte
    images = []
    for img_data in [img1_data, img2_data, img3_data]:
        if img_data:
            image = Image.open(BytesIO(img_data)).convert("RGBA")
            images.append(image)

    # Provjeri da imamo barem jednu sliku
    if not images:
        print("❌ Nema valjanih slika za GIF.")
    else:
        duration = 500  # trajanje svakog frame-a u ms
        images[0].save("images/output.gif", save_all=True,
                       append_images=images[1:], duration=duration, loop=0)
        print("✅ GIF spremljen u: images/output.gif")

def resizeImage4Share(name):
    # New image size
    new_size = (1500, 1000)
    # Open image
    image = Image.open(name)
    # Get image info
    exif = image.info['exif']
    # resize with Lanczos method
    resized_image = image.resize(new_size, resample = Image.LANCZOS)
    resized_image.save(name, quality=96, exif=exif)
