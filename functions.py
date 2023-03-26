import cloudinary
from cloudinary.uploader import upload
import time
import cups
from PIL import Image
import qrcode
import json

# ucitavanje config.jsona i metanje u varijable da se lakse koristi
with open('config.json', 'r') as f:
    # Load the contents of the file into a dictionary
    config = json.load(f)
eventId = config['eventId']

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


def uploadToAlbum(brojSlike, eventId):
    upload("res/session/slika" + str(brojSlike) + ".jpg",
           public_id="djenka/" + eventId + "/album/" + str(time.time()))


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
    print('printam dve kartice')

    if kolKartica == 4:
        conn.printFile(
            PrinterUsing, "res/session/dupla_kartica.png", "title", emptyDict)
        print('printam JOS dve kartice')


def napraviKarticu(eventId):

    kartica = Image.open('res/event/'+eventId+'/kartica.png')
    im1 = Image.open('res/session/slika1.jpg').resize((800, 533))
    im2 = Image.open('res/session/slika2.jpg').resize((800, 533))
    im3 = Image.open('res/session/slika3.jpg').resize((800, 533))

    kartica.paste(im1, (100, 187))
    kartica.paste(im2, (100, 877))
    kartica.paste(im3, (100, 1567))

    kartica.save('res/session/gotovaKartica.png')


def napraviQr(eventId):
    img = qrcode.make('www.djenka.tk/' + eventId)
    type(img)  # qrcode.image.pil.PilImage
    img.save("res/event/" + eventId + "/qr.png")
