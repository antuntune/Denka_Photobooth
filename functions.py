import cloudinary
from cloudinary.uploader import upload
import time
import cups
from PIL import Image

cloudinary.config(
    cloud_name="dpuhwc49z",
    api_key="544431793628367",
    api_secret="jXcv2cki8LffeJ1Wz-FOrYU4sd8",
    secure=True
)


conn = cups.Connection()
printers = conn.getPrinters()
# printers is a dictionary containing information about all the printers available

emptyDict = {}
AvailablePrinters = list(printers.keys())
PrinterUsing = AvailablePrinters[0]


def uploadToAlbum(brojSlike):
    upload("res/session/slika" + str(brojSlike) + ".jpg",
           public_id="djenka/saraiantonio2904/album/" + str(time.time()))


def printaj(kolKartica):
    im1 = Image.open('res/session/gotovaKartica.png')

    def get_concat_h(im1):
        dst = Image.new('RGB', (im1.width + im1.width + 35, im1.height))
        dst.paste(im1, (35, 0))
        dst.paste(im1, (im1.width + 35, 0))
        return dst

    get_concat_h(im1).save('res/session/dupla_kartica.png')

    conn.printFile(
        PrinterUsing, "res/session/dupla_kartica.png", "title", emptyDict)

    if kolKartica == 4:
        conn.printFile(
            PrinterUsing, "res/session/dupla_kartica.png", "title", emptyDict)


def napraviKarticu():

    kartica = Image.open('res/event/kartica.png')
    im1 = Image.open('res/session/slika1.jpg').resize((800, 533))
    im2 = Image.open('res/session/slika2.jpg').resize((800, 533))
    im3 = Image.open('res/session/slika3.jpg').resize((800, 533))

    kartica.paste(im1, (100, 187))
    kartica.paste(im2, (100, 877))
    kartica.paste(im3, (100, 1567))

    kartica.save('res/session/gotovaKartica.png')
